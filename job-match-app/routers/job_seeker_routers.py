import io
from typing import Annotated

from fastapi.responses import JSONResponse, StreamingResponse

from app_models.validation_models import ALLOWED_PASSWORD
from services import job_seeker_services, upload_services
from fastapi import APIRouter, Query, Depends, Form
from fastapi.responses import JSONResponse
from services import job_seeker_services
from app_models.job_seeker_models import *
from common.auth import get_current_user
from common.country_validators_helpers import validate_location, validate_city
from common.separators_validators import parse_skills
from fastapi import HTTPException

job_seekers_router = APIRouter(prefix='/seekers')


@job_seekers_router.get('/', description= 'You can view every available job seeker in this section.', 
                        tags=['Seeker Section'])

def get_all_seekers(current_user_payload=Depends(get_current_user)):

    if current_user_payload['group'] != 'seekers':
        raise HTTPException(status_code=403,
                            detail='Only seekers can view all seekers')

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


@job_seekers_router.get('/personal_info', description= 'You can view your personal information in this section.', 
                        tags=['Seeker Section'])

def your_information(current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='Only seekers can get personal info them')
    
    username = current_user_payload.get('username')
    job_seeker = JobSeekerOptionalInfo()
    job_seeker.username = username

    if not job_seeker_services.check_seeker_exists(job_seeker.username):
        raise HTTPException(status_code=404, detail='No seeker found in the system!')

    current_job_seeker_info = job_seeker_services.job_seeker_info_username(job_seeker.username)

    return current_job_seeker_info


@job_seekers_router.put('/information/edit', description= 'You can edit your personal information in this section.', tags=['Seeker Section'])
def edit_proffesional_info(summary: str = Form(None),
                           telephone: str = Form(None),
                           address: str = Form(None),
                           city: str = Form(None),
                           current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'seekers':
        raise HTTPException(status_code=403,
                            detail='Only seekers can edit their info')
    
    username = current_user_payload.get('username')
    
    db_seeker = job_seeker_services.get_job_seeker_info(username)
    job_seeker = JobSeekerOptionalInfo()
    contacts = job_seeker_services.location_id_from_contacts(db_seeker[0][10])
    db_location = job_seeker_services.location_finder(contacts[0][0])
    job_seeker.username = username
    job_seeker.summary = summary or db_seeker[0][5]
    job_seeker.telephone = telephone or contacts[0][2]
    job_seeker.address = address or contacts[0][1]
    job_seeker.city = city or db_location[0][0]

    if not summary and not city and not address and not telephone:
        raise HTTPException(status_code=203,detail= "You haven't done any changes to your personal information")

    validate_city(job_seeker.city)
    
    return job_seeker_services.edit_info(job_seeker.username, job_seeker.summary,job_seeker.city, job_seeker.telephone, job_seeker.address)


@job_seekers_router.post('/cv', description= 'You can create your cvs from this section.', 
                         tags =['CV Section'])

def create_cv(description: str = Form(),
              min_salary: int = Form(),
              max_salary: int = Form(),
              location: str = Form(None),
              is_remote: str = Form(enum=['Yes', 'No']),
              skills: str = Form(description='Example: python;3,java;2,javascript;1 [1 - Beginner, 2 - Intermidiate, 3 - Advanced]'),
              current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'seekers':
        raise HTTPException(status_code=403,
                            detail='Only seekers can create cv')
    
    validate_city(location)
    
    status = 'Private'
    is_main_cv = False
    seeker_username = current_user_payload.get('username')
    seeker_id = current_user_payload.get('id')
    seeker_id = job_seeker_services.get_job_seeker_info(seeker_username)
    skill_list = parse_skills(skills)

    if min_salary and max_salary:
        if min_salary > max_salary:
            raise HTTPException(status_code=400, detail='The minimum salary cannot be bigger than the maximum salary')

    try:
        skill_names = [skill.split(';')[0] for skill in skill_list]
        skill_levels = [skill.split(';')[1] for skill in skill_list]
    except IndexError:
        raise HTTPException(status_code=400, detail='Invalid input look at the description')
    
    if len(skill_list) < 2:
        raise HTTPException(status_code=400, detail='You need atleast 2 skills!')
    if len(skill_list) > 5:
        raise HTTPException(status_code=400, detail='The maximum skill limit of 5 has been reached!')
    
    return job_seeker_services.create_cv(description, location, is_remote, min_salary, max_salary, 
                                         status,seeker_id[0][0], skill_names, skill_levels, is_main_cv)


@job_seekers_router.put('/cv/edit', description= 'You can edit your cvs from this section.', 
                        tags =['CV Section'])

@job_seekers_router.put('/cv/edit', description= 'You can edit your cvs from this section.', tags =['CV Section'])
def edit_cv(cv_id: int = Form(),description: str = Form(None), min_salary: int = Form(None),
            max_salary: int = Form(None), status: str =  Form(enum=['Active', 'Hidden', 'Private']),
            skills: str = Form(None, description = 'Example: python;3,java;2,javascript;1 [1 - Beginner, 2 - Intermidiate, 3 - Advanced]'),
            current_user_payload=Depends(get_current_user)):

    if current_user_payload['group'] != 'seekers':
        raise HTTPException(status_code=403,
                            detail='Only seekers can create cv')
    
    seeker_id = current_user_payload.get('id')

    
    if job_seeker_services.check_is_matched(cv_id) and status:
        raise HTTPException(status_code=400, detail='You cant modify your status when is matched already')
    
    if not status:
        status = job_seeker_services.get_existing_status(cv_id)

    if not job_seeker_services.check_owner_cv(cv_id,seeker_id):
        raise HTTPException(status_code=400, detail='That id is not a valid for your cvs')
    
    try:
        skill_list = parse_skills(skills)
        skill_names = [skill.split(';')[0] for skill in skill_list]
        skill_levels = [skill.split(';')[1] for skill in skill_list]

    except IndexError:
        raise HTTPException(status_code=400, detail='Invalid input look at the description')
    except TypeError:
        cv_skills_info_ids = job_seeker_services.get_existing_skills(cv_id)
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
            raise HTTPException(status_code=400, detail='The minimum salary cannot be bigger than the maximum salary')
    if min_salary:
        if min_salary > cv_info[0][2]:
            raise HTTPException(status_code=400, detail="Your maximum salary is low change it if you wan't to change the minimum")

    arg_min_salary = min_salary or cv_info[0][1]
    arg_max_salary = max_salary or cv_info[0][2]
    arg_description = description or cv_info[0][3]
    if not description and not min_salary and not max_salary and not skills:
        raise HTTPException(status_code=202, detail="You haven't done any changes to your CV information")

    return job_seeker_services.edit_cv(seeker_id, cv_id, arg_min_salary, arg_max_salary, 
                                       arg_description, status, skill_names, skill_levels)


@job_seekers_router.get('/cv', description= 'You can view your cvs from this section.', 
                        tags =['CV Section'])

def view_personal_cvs(current_user_payload=Depends(get_current_user)):

    if current_user_payload['group'] != 'seekers':
        raise HTTPException(status_code=403,
                            detail='Only seekers can view cvs')
    

    seeker_id = current_user_payload.get('id')
    return job_seeker_services.view_personal_cvs(seeker_id)


@job_seekers_router.post('/register', description= 'You can register with your personal information in this section.', 
                         tags=['Seeker & Company Signup'])

def add_seeker(seeker_username: Annotated[ALLOWED_USERNAME, Form()],
              seeker_password: Annotated[ALLOWED_PASSWORD, Form()],
              seeker_first_name: str = Form(), 
              seeker_last_name: str = Form(),
              seeker_email_adress: str = Form(),
              seeker_telephone : str = Form(),
              seeker_address: str = Form(),
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
    current_seeker.telephone = seeker_telephone
    current_seeker.address = seeker_address

    

    if job_seeker_services.check_seeker_exists(current_seeker.username):
        raise HTTPException(status_code=409,
                            detail=f'Seeker with username {current_seeker.username} already exists.')

    new_seeker = job_seeker_services.create_seeker(current_seeker.username, current_seeker.password, current_seeker.first_name, current_seeker.last_name,
                                                   current_seeker.email, current_seeker.city, current_seeker.country, current_seeker.telephone, current_seeker.address)
    return new_seeker


@job_seekers_router.get('/search/job_ads', description= 'You can search specific job ads in this section by their salary.', 
                        tags=['Seeker Matching Section'])

def search_job_ads_by_status(current_user_payload=Depends(get_current_user),
                              sort_percent: str =  Query(enum=['Best', 'Very good', 'Good', 'Bad', 'Worst'])):

    if current_user_payload['group'] != 'seekers':
        raise HTTPException(status_code=403,
                            detail='Only seekers can search job ads')

    job_seeker_id = current_user_payload.get('id')


    return job_seeker_services.calculate_percents_job_ad(job_seeker_id, sort_percent, 
                                                         threshold_percent= None, perms = 'Seeker')


@job_seekers_router.get('/sorting_salary', description= 'You can search job ads by salary range in this section.', 
                        tags =['Seeker Matching Section'])

def search_job_ads_by_salary(current_user_payload=Depends(get_current_user),
                              min_salary: int = Query(), max_salary: int = Query(),
                              threshold_percent: int = Query()):

    if current_user_payload['group'] != 'seekers':
        return JSONResponse(status_code=403,
                            content='Only seekers can search job ads')
    
    if threshold_percent > 100:
        raise HTTPException(status_code=400, detail='The threshold should be lower than 100%')

    job_seeker_id = current_user_payload.get('id')
    sort_percent = 'All'
    salary_input = [min_salary, max_salary]
    perms = 'Seeker'

    return job_seeker_services.calculate_percents_job_ad(job_seeker_id, sort_percent, perms, 
                                                         threshold_percent, salary_input)
    

@job_seekers_router.get('/companies/job_ads', description= 'You can view every specific company job ad from this section.', 
                        tags =['Seeker Section'])

def get_job_ads_from_companies(current_user_payload=Depends(get_current_user)):

    if current_user_payload['group'] != 'seekers':
        raise HTTPException(status_code=403,
                            detail='This option is only available for Job_Seekers')
    return job_seeker_services.get_all_job_ads()


@job_seekers_router.get('{id}/avatar', description= 'You can view a specific job seeker avatar from this section.', 
                        tags=['Seeker Section'])

def get_seeker_avatar(id: int, current_user_payload=Depends(get_current_user)):
    image_data = upload_services.get_picture(id, 'admins')

    if not job_seeker_services.seeker_exists_by_id(id):
        raise HTTPException(status_code=404,
                            detail='No such job seeker.')
    if image_data is None:
        raise HTTPException(status_code=404,
                            detail='No picture associated with the job seeker.')

    return StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")


@job_seekers_router.put('/main_cv', description= 'You can choose a main cv from this section.', 
                        tags=['CV Section'])

def select_main_cv(cv_id: int = Query(), current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'seekers':
        raise HTTPException(status_code=403,
                            detail='Only seekers can search job ads')
    
    seeker_id = current_user_payload.get('id')
    
    if not job_seeker_services.check_owner_cv(cv_id,seeker_id):
        raise HTTPException(status_code=400, detail='That id is not a valid for your cvs')
    
    if job_seeker_services.is_main_already(cv_id):
        raise HTTPException(status_code=202, detail='This CV is already main!')
    

    return job_seeker_services.update_main_cv(cv_id, seeker_id)
