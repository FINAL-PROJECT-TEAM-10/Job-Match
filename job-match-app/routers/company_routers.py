from fastapi import APIRouter, Query, Body,Header, HTTPException
from fastapi.responses import JSONResponse
from services import company_services

companies_router = APIRouter(prefix='/companies',tags={'Everything available for Companies'})

@companies_router.get('/', description= 'You can view every company from here')
def view_all_companies():

    get_companies = company_services.read_companies()
    result = []

    for data in get_companies:
        get_companies_info = company_services.read_company_adress(data[0])
        data_dict = {
            "Company Name": data[1],
            "Email": get_companies_info[0][1],
            "Work Adress": get_companies_info[0][2],
            "Telephone": get_companies_info[0][3],
            "City Postal Code": get_companies_info[0][4]
        }
         
        result.append(data_dict)

    return result