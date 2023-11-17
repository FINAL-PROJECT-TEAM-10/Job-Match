from fastapi import APIRouter, Query,Depends
from services import job_ads_services
from fastapi.responses import JSONResponse
from common.auth import get_current_user
from services import company_services
from common.separators_validators import parse_skills

job_ads_router = APIRouter(prefix='/job_ads',tags={'Everything available for Job_Ads'})

@job_ads_router.post('/')
def create_new_job_ad(description: str = Query(), min_salary: int = Query(),max_salary: int = Query(), 
                      requirements: str = Query(description='Example: python;3,java;2,javascript;1 [1 - Beginner, 2 - Intermidiate, 3 - Advanced]'),
                      current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'companies':
        return JSONResponse(status_code=403,
                            content='This option is only available for Companies')
    
    status = 'active'
    requirements_list = parse_skills(requirements)
    try:
        requirements_names = [skill.split(';')[0] for skill in requirements_list]
        requirements_levels = [skill.split(';')[1] for skill in requirements_list]
    except IndexError:
        return JSONResponse(status_code=404,content='Invalid input look at the description')

    if len(requirements_list) < 2:
        return JSONResponse(status_code=400, content='You need atleast 2 requirements!')
    if len(requirements_list) > 5:
        return JSONResponse(status_code=400, content='The maximum requirements limit of 5 has been reached!')

    company_username = current_user_payload.get('username')
    company_id = job_ads_services.find_company(company_username)

    create_job = job_ads_services.create_job_add(description,min_salary,max_salary,status,company_id[0][0],requirements_names,requirements_levels)
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

@job_ads_router.put('/edit/information')
def edit_your_job_ad(job_ad_id: str = Query(), description: str = Query(None), min_salary: int = Query(None), 
                     max_salary: int = Query(None), requirements: str = Query(None), current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'companies':
        return JSONResponse(status_code=403,
                            content='This option is only available for Companies')
    
    company_id = current_user_payload.get('id')

    if not job_ads_services.check_owner_company(job_ad_id,company_id):
        return JSONResponse(status_code=400, content='That id is not a valid for your job_ads')
    
    if max_salary < min_salary:
        return JSONResponse(status_code=400, content='The minimum salary cannot be bigger than the maximum salary')
    # requirements_list = parse_skills(requirements)

    # try:
    #     requirements_names = [skill.split(';')[0] for skill in requirements_list]
    #     requirements_levels = [skill.split(';')[1] for skill in requirements_list]
    # except IndexError:
    #     return JSONResponse(status_code=404,content='Invalid input look at the description')
    
    company_information = job_ads_services.check_company_information(company_id, job_ad_id)

    arg_min_salary = min_salary or company_information[0][1]
    arg_max_salary = max_salary or company_information[0][2]
    arg_description = description or company_information[0][3]

    return job_ads_services.edit_job_ads(company_id, job_ad_id, arg_min_salary,arg_max_salary,arg_description)