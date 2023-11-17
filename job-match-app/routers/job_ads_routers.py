from fastapi import APIRouter, Query,Depends
from services import job_ads_services
from fastapi.responses import JSONResponse
from common.auth import get_current_user
from services import company_services

job_ads_router = APIRouter(prefix='/job_ads',tags={'Everything available for Job_Ads'})

@job_ads_router.post('/')
def create_new_job_ad(description: str = Query(), min_salary: int = Query(),max_salary: int = Query(),
                      current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'companies':
        return JSONResponse(status_code=403,
                            content='This option is only available for Companies')
    
    status = 'active'
    company_username = current_user_payload.get('username')
    company_id = job_ads_services.find_company(company_username)

    create_job = job_ads_services.create_job_add(description,min_salary,max_salary,status,company_id[0][0])
    return create_job

@job_ads_router.get('/companies')
def view_different_company_ads(name_of_company: str = Query(), current_user_payload=Depends(get_current_user)):
    
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

@job_ads_router.get('/information')
def view_your_company_ads(current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'companies':
        return JSONResponse(status_code=403,
                            content='This option is only available for Companies')
    
    company_ads = current_user_payload.get('username')

    company_id = job_ads_services.find_company(company_ads)
    get_company_ads = job_ads_services.view_job_ads_by_id(company_id[0][0])

    return get_company_ads