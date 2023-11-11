from fastapi import APIRouter, Query, Body,Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from services import company_services
from app_models.company_models import Company
from typing import Annotated
from common.auth import get_current_user

companies_router = APIRouter(prefix='/companies',tags={'Everything available for Companies'})

@companies_router.get('/', description= 'You can view every company from here')
def view_all_companies():

    get_companies = company_services.read_companies()
    result = []

    for data in get_companies:
        get_companies_info = company_services.read_company_adress(data[0])
        get_companies_location = company_services.read_company_location(get_companies_info[0][5])
        data_dict = {
            "Company Name": data[1],
            "Email": get_companies_info[0][1],
            "Work Adress": get_companies_info[0][2],
            "Telephone": get_companies_info[0][3],
            "City": get_companies_location[0][1],
            "City Postal Code": get_companies_info[0][4],
            "Country": get_companies_location[0][0]
        }
         
        result.append(data_dict)

    return result

@companies_router.post('/register', response_model=Company)
def company_registration(Company_Name: str = Query(), Password: str = Query(), 
                         Company_City: str = Query(), Company_Country: str = Query(), Company_Adress: str = Query(),
                         Telephone_Number: int = Query(),Email_Adress: str = Query(),):
    

    if company_services.check_company_exist(Company_Name):
        return JSONResponse(status_code=409,content=f'Company with this {Company_Name} already exists.')

    create_company = company_services.create_company(Company_Name, Password, Company_City, Company_Country, 
                                                     Company_Adress, Telephone_Number, Email_Adress)
    
    return create_company



@companies_router.get('/information')
def your_company_information(company: str):

    company_info = company_services.read_company_information(company)
    
    return Company(company_name=company_info.company_name,email = company_info.company_name, work_adress = company_info.company_name, 
                   telephone = company_info.company_name, country = company_info.company_name, city = company_info.company_name)