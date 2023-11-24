from fastapi import APIRouter, Query, Depends, Form
from fastapi.responses import JSONResponse
from services import job_seeker_services
from app_models.job_seeker_models import *
from common.auth import get_current_user
from common.country_validators_helpers import validate_location, validate_city
from common.separators_validators import parse_skills
from fastapi.responses import HTMLResponse

job_seekers_router = APIRouter(prefix='/job_seekers')


@job_seekers_router.get('/', description= 'All functions for job seekers', tags=['Seeker Section'])
def get_all_seekers(current_user_payload=Depends(get_current_user)):

    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='Only seekers can view all seekers')


    get_seekers = job_seeker_services.read_seekers()

    result = []

    for data in get_seekers:
        seeker_contacts = job_seeker_services.contacts_info_for_seeker(data[10])
        seeker_location = job_seeker_services.location_finder(seeker_contacts[0][3])
        data_dict = {
            "Username": data[1],
            "Email": seeker_contacts [0][0],
            'Adress': seeker_contacts[0][1],
            'Telephone': seeker_contacts[0][2],
            'City': seeker_location[0][0],
            'Country': seeker_location[0][1],

        }

        result.append(data_dict)
    

    return result


@job_seekers_router.get('/personal_info', tags=['Seeker Section'])
def your_information(current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='Only seekers can get personal info them')
    
    username = current_user_payload.get('username')
    job_seeker = JobSeekerOptionalInfo()
    job_seeker.username = username

    if not job_seeker_services.check_seeker_exists(job_seeker.username):
        return JSONResponse(status_code=404, content='No seeker found in the system!')

    current_job_seeker_info = job_seeker_services.job_seeker_info_username(job_seeker.username)

    return current_job_seeker_info


@job_seekers_router.put('/personal_info/edit', tags=['Seeker Section'])
def edit_proffesional_info(summary: str = Query(None),
                           city: str = Query(None),
                           status: str =  Query(enum=['Active', 'Busy']),
                           current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='Only seekers can edit their info')
    
    username = current_user_payload.get('username')
    
    db_seeker = job_seeker_services.get_job_seeker_info(username)
    job_seeker = JobSeekerOptionalInfo()
    contacts = job_seeker_services.location_id_from_contacts(db_seeker[0][10])
    db_location = job_seeker_services.location_finder(contacts)
    job_seeker.username = username
    job_seeker.summary = summary or db_seeker[0][5]
    job_seeker.city = city or db_location[0][0]
    job_seeker.status = status

    validate_city(job_seeker.city)
    
    return job_seeker_services.edit_info(job_seeker.username, job_seeker.summary,job_seeker.city,job_seeker.status)

@job_seekers_router.post('/cv', tags=['CV Section'])
def create_cv(description: str = Query(),
              min_salary: int = Query(),
              max_salary: int = Query(),
              skills: str = Query(description='Example: python;3,java;2,javascript;1 [1 - Beginner, 2 - Intermidiate, 3 - Advanced]'),
              current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='Only seekers can create cv')
    
    status = 'Active'
    is_main_cv = False
    seeker_username = current_user_payload.get('username')
    seeker_id = current_user_payload.get('id')
    seeker_id = job_seeker_services.get_job_seeker_info(seeker_username)
    skill_list = parse_skills(skills)#['python;2', 'javascript;3']

    if min_salary and max_salary:
        if min_salary > max_salary:
            return JSONResponse(status_code=400, content='The minimum salary cannot be bigger than the maximum salary')

    try:
        skill_names = [skill.split(';')[0] for skill in skill_list]
        skill_levels = [skill.split(';')[1] for skill in skill_list] #[2,3]
    except IndexError:
        return JSONResponse(status_code=400, content='Invalid input look at the description')
    
    if len(skill_list) < 2:
        return JSONResponse(status_code=400, content='You need atleast 2 skills!')
    if len(skill_list) > 5:
        return JSONResponse(status_code=400, content='The maximum skill limit of 5 has been reached!')
    
    return job_seeker_services.create_cv(description,min_salary,max_salary,status,seeker_id[0][0], skill_names, skill_levels, is_main_cv)

@job_seekers_router.put('/cv/edit', tags=['CV Section'])
def edit_cv(cv_id: int = Query(),description: str = Query(None), min_salary: int = Query(None),
            max_salary: int = Query(None), status: str =  Query(enum=['Active', 'Hidden', 'Private']),
            skills: str = Query(None),
            current_user_payload=Depends(get_current_user)):

    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='Only seekers can create cv')
    
    seeker_id = current_user_payload.get('id')
    

    if not job_seeker_services.check_owner_cv(cv_id,seeker_id):
        return JSONResponse(status_code=400, content='That id is not a valid for your cvs')
    
    try:
        skill_list = parse_skills(skills)
        skill_names = [skill.split(';')[0] for skill in skill_list]
        skill_levels = [skill.split(';')[1] for skill in skill_list] #[2,3]
    except IndexError:
        return JSONResponse(status_code=400, content='Invalid input look at the description')
    except TypeError:
        cv_skills_info_ids = job_seeker_services.get_existing_skills(cv_id) #2,10
        skill_names = []
        skill_levels = []

        try:
            for skill_id in cv_skills_info_ids[0]:
                current_name = job_seeker_services.find_skill_name_by_id(skill_id)
                skill_names.append(current_name)
                current_skill_level = job_seeker_services.find_level_by_ids(cv_id, skill_id)
                skill_levels.append(current_skill_level)
        except IndexError:
            skill_names = []
            skill_list = []

    cv_info = job_seeker_services.get_cv_info(seeker_id, cv_id)

    if min_salary and max_salary:
        if min_salary > max_salary:
            return JSONResponse(status_code=400, content='The minimum salary cannot be bigger than the maximum salary')
    if min_salary:
        if min_salary > cv_info[0][2]:
            return JSONResponse(status_code=400, content="Your maximum salary is low change it if you wan't to change the minimum")

    arg_min_salary = min_salary or cv_info[0][1]
    arg_max_salary = max_salary or cv_info[0][2]
    arg_description = description or cv_info[0][3]
    if not description and not min_salary and not max_salary and not skills:
        return JSONResponse(status_code=202, content="You haven't done any changes to your CV information")

    return job_seeker_services.edit_cv(seeker_id, cv_id, arg_min_salary,arg_max_salary,arg_description, status, skill_names, skill_levels)


@job_seekers_router.get('/cv', tags=['CV Section'])
def view_personal_cvs(current_user_payload=Depends(get_current_user)):

    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='Only seekers can view cvs')
    

    username = current_user_payload.get('username')
    seeker_id = job_seeker_services.get_job_seeker_info(username)
    return job_seeker_services.view_personal_cvs(seeker_id[0][0])


@job_seekers_router.post('/register', tags=['Seeker & Company Signup'])
def add_seeker(seeker_username: str = Form(),
              seeker_password: str = Form(),
              seeker_first_name: str = Form(), 
              seeker_last_name: str = Form(),
              seeker_email_adress: str = Form(),
              seeker_city: str = Form(),
              seeker_country: str = Form()):
    
    validate_location(seeker_city, seeker_country)

    
    current_seeker = JobSeekerOptionalInfo()
    current_seeker.username = seeker_username
    current_seeker.password = seeker_password
    current_seeker.first_name = seeker_first_name
    current_seeker.last_name = seeker_last_name
    current_seeker.email = seeker_email_adress
    current_seeker.city = seeker_city
    current_seeker.country = seeker_country
    

    if job_seeker_services.check_seeker_exists(current_seeker.username):
        return JSONResponse(status_code=409,
                            content=f'Seeker with username {current_seeker.username} already exists.')

    new_seeker = job_seeker_services.create_seeker(current_seeker.username, current_seeker.password, current_seeker.first_name, current_seeker.last_name,
                                                   current_seeker.email, current_seeker.city, current_seeker.country)
    return new_seeker


@job_seekers_router.get('/search/job_ads', tags=['Seeker Section'])
def search_job_ads_percentage(current_user_payload=Depends(get_current_user),
                              sort_percent: str =  Query(enum=['Best', 'Very good', 'Good', 'Bad', 'Worst'])):

    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='Only seekers can search job ads')

    job_seeker_id = current_user_payload.get('id')


    return job_seeker_services.calculate_percents_job_ad(job_seeker_id, sort_percent, perms = 'Seeker')


@job_seekers_router.get('/sorting_salary', tags=['Seeker Section'])
def search_job_ads_by_salary(current_user_payload=Depends(get_current_user),
                              min_salary: int = Query(), max_salary: int = Query()):

    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='Only seekers can search job ads')

    job_seeker_id = current_user_payload.get('id')
    sort_percent = 'All'
    salary_input = [min_salary, max_salary]
    perms = 'Seeker'

    return job_seeker_services.calculate_percents_job_ad(job_seeker_id, sort_percent,perms, salary_input)
    

@job_seekers_router.get('/companies/job_ads',tags=['Seeker Section'])
def get_job_ads_from_companies(current_user_payload=Depends(get_current_user)):

    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='This option is only available for Job_Seekers')
    return job_seeker_services.get_all_job_ads()



@job_seekers_router.get('/main_cv', tags=['CV Section'])
def select_main_cv(cv_id: int = Query(), current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='Only seekers can search job ads')
    
    seeker_id = current_user_payload.get('id')
    
    if not job_seeker_services.check_owner_cv(cv_id,seeker_id):
        return JSONResponse(status_code=400, content='That id is not a valid for your cvs')
    

    return job_seeker_services.update_main_cv(cv_id, seeker_id)