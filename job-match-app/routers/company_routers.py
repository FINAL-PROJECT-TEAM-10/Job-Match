from fastapi import APIRouter, Query, Body,Header, HTTPException
from fastapi.responses import JSONResponse
from services import company_services
from app_models.company_models import Company

companies_router = APIRouter(prefix='/companies',tags={'Everything available for Companies'})

@companies_router.get('/', description= 'You can view every company from here')
def view_all_companies():

    get_companies = company_services.read_companies()
    result = []

    for data in get_companies:
        get_companies_info = company_services.read_company_adress(data[0])
        get_companies_location = company_services.read_company_location(data[0])
        data_dict = {
            "Company Name": data[1],
            "Email": get_companies_info[0][1],
            "Work Adress": get_companies_info[0][2],
            "Telephone": get_companies_info[0][3],
            "Country": get_companies_location[0][0],
            "City": get_companies_location[0][1],
            "City Postal Code": get_companies_info[0][4]
        }
         
        result.append(data_dict)

    return result

@companies_router.get('/information')
def your_company_information(company: str):

    company_info = company_services.read_company_information(company)
    
    return Company(company_name=company_info.company_name,email = company_info.company_name, work_adress = company_info.company_name, 
                   telephone = company_info.company_name, country = company_info.company_name, city = company_info.company_name)