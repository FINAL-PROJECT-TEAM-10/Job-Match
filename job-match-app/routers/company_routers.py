import io
from fastapi import APIRouter, Query,Depends
from fastapi.responses import JSONResponse, StreamingResponse
from services import company_services, upload_services
from fastapi import APIRouter, Query,Depends,Form
from fastapi.responses import JSONResponse
from services import company_services
from services import job_ads_services
from app_models.company_models import Company
from common.auth import get_current_user
from common.country_validators_helpers import *

companies_router = APIRouter(prefix='/companies')

@companies_router.get('/', description= 'You can view every company from here', tags=['Company Section'])
def view_all_companies(current_user_payload=Depends(get_current_user)):
    if current_user_payload['group'] != 'companies':
        return JSONResponse(status_code=403,
                            content='This option is only available for Companies')
    
    get_companies = company_services.read_companies()
    result = []

    for data in get_companies:
        get_companies_info = company_services.read_company_adress(data[0])
        get_companies_location = company_services.read_company_location(get_companies_info[0][4])
        data_dict = {
            "Company Name": data[1],
            "Email": get_companies_info[0][1],
            "Work Adress": get_companies_info[0][2],
            "Telephone": get_companies_info[0][3],
            "City": get_companies_location[0][0],
            "Country": get_companies_location[0][1]
        }
         
        result.append(data_dict)

    return result

@companies_router.post('/register', response_model=Company, tags=['Seeker & Company Signup'])
def company_registration(Company_Name: str = Form(), Password: str = Form(), 
                         Company_City: str = Form(), Company_Country: str = Form(), Company_Adress: str = Form(),
                         Telephone_Number: int = Form(),Email_Adress: str = Form(),):
    
    validate_location(Company_City, Company_Country)

    if company_services.check_company_exist(Company_Name):
        return JSONResponse(status_code=409,content=f'Company with this {Company_Name} already exists.')

    create_company = company_services.create_company(Company_Name, Password, Company_City, Company_Country, 
                                                     Company_Adress, Telephone_Number, Email_Adress)
    
    return create_company


@companies_router.get('/information', tags=['Company Section'])
def your_company_information(current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'companies':
            return JSONResponse(status_code=403,
                                content='This option is only available for Companies')  
    
    company_name = current_user_payload.get('username')

    all_information = []
    
    get_company_information = company_services.get_company_info_name(company_name)
    company_id = company_services.find_company_id_byusername(company_name)
    get_location_id = company_services.location_id(company_id)
    company_location_from_id = company_services.find_location(get_location_id)
    count_active_job_ads = job_ads_services.get_current_active_job_ads(company_id)
    company_contacts = company_services.read_company_adress(company_id)
    matched_job_ads = company_services.find_matched_job_ads(company_id)
    
    description = get_company_information[0][1]
    
    if not description:
        description = 'There is no current description set for this company'

    company_dict = {
        
         "Company Name": get_company_information[0][0],
         "Company Description": description,
         "Company Email": company_contacts[0][1],
         "Company Address": company_contacts[0][2],
         "Company Telephone": company_contacts[0][3],
         "Company City": company_location_from_id[0][0],
         "Company Country": company_location_from_id[0][1],
         "Active job ads": count_active_job_ads,
         "Matched job ads": matched_job_ads

    }

    all_information.append(company_dict)

    return all_information

@companies_router.put('/information/edit', tags=['Company Section'])
def edit_your_company_information(description: str = Query(None),
                             city: str = Query(None),
                             address: str = Query(None),
                             telephone: int = Query(None),
                             current_user_payload=Depends(get_current_user)
                             ):
     
    if current_user_payload['group'] != 'companies':
        return JSONResponse(status_code=403,
                            content='This option is only available for Companies')
     
    username = current_user_payload.get('username')

    company_info = company_services.everything_from_companies_by_username(username)
    location_id = company_services.location_id(company_info[0][0])
    get_city_and_country_for_company = company_services.find_location(location_id)
    get_company_contacts = company_services.read_company_adress(company_info[0][0])
    
    final_company_description = description or company_info[0][3]
    final_company_city = city or get_city_and_country_for_company[0][0]
    final_company_adress = address or get_company_contacts[0][2]
    final_company_telephone = telephone or get_company_contacts[0][3]
    
    if not description and not city and not address and not telephone:
        return JSONResponse(status_code=203,content= "You haven't done any changes to your personal company information")

    validate_city(final_company_city)

    return company_services.edit_company_information(username, final_company_description, final_company_city, final_company_adress, final_company_telephone)

@companies_router.get('/job_seekers/cv', tags=['Company Section'])
def get_cv_from_job_seeker(current_user_payload=Depends(get_current_user)):

    if current_user_payload['group'] != 'companies':
        return JSONResponse(status_code=403,
                            content='This option is only available for Companies')

    return company_services.view_all_cvs()


# TODO: test below for companies (low priority)
@companies_router.get('{id}/avatar', tags=['Company Section'])
def get_company_avatar(id: int, current_user_payload=Depends(get_current_user)):
    image_data = upload_services.get_picture(id, 'companies')

    if not company_services.company_exists_by_id(id):
        return JSONResponse(status_code=404,
                            content='No such company.')
    if image_data is None:
        return JSONResponse(status_code=404,
                            content='No picture associated with the company.')

    return StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")

