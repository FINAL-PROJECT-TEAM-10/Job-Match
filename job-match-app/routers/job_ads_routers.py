from fastapi import APIRouter, Query, Body,Header, HTTPException,Depends
from services import job_ads_services
from fastapi.responses import JSONResponse
from common.auth import get_current_user

job_ads_router = APIRouter(prefix='/job_ads',tags={'Everything available for Job_Ads'})

@job_ads_router.post('/')
def create_new_job_ad(description: str = Query(), min_salary: int = Query(),max_salary: int = Query(),
                      status: str = Query(),date_posted: str = Query(), name_of_company: str = Query(),current_user_payload=Depends(get_current_user)):
    if current_user_payload['group'] != 'companies':
        return JSONResponse(status_code=403,
                            content='This option is only available for Companies')
    
    if not job_ads_services.check_company_exist(name_of_company):
        return JSONResponse(status_code=404,content='This name doesnt exist')
    create_job = job_ads_services.create_job_add(description,min_salary,max_salary,status,date_posted,name_of_company)
    return create_job

@job_ads_router.get('/information')
def view_your_company_ads(name_of_company: str = Query(), current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'companies':
        return JSONResponse(status_code=403,
                            content='This option is only available for Companies')
    
    if not job_ads_services.check_company_exist(name_of_company):
        return JSONResponse(status_code=404,content='This company name doesnt exist')
    view_ads = job_ads_services.view_all_job_ads(name_of_company)

    result = []

    for data in view_ads:
        data_dict = {
            "Description": data[1],
            "Minimum Salary": data[2],
            "Maximum Salary": data[3],
            "Status": data[4],
            "Date Posted": data[5]
        }
         
        result.append(data_dict)

    return result
