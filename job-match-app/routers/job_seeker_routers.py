from fastapi import APIRouter, Query,HTTPException, Depends
from fastapi.responses import JSONResponse
from services import job_seeker_services
from app_models.job_seeker_models import *
from typing import Annotated
from common.auth import get_current_user
from common.country_validators_helpers import validate_location, validate_city

job_seekers_router = APIRouter(prefix='/job_seekers',tags={'Job seekers'})


@job_seekers_router.get('/', description= 'All functions for job seekers')
def get_all_seekers(current_user_payload=Depends(get_current_user)):

    if current_user_payload['group'] != 'admins':
        return JSONResponse(status_code=403,
                            content='Only  admins can view all seekers')


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


@job_seekers_router.get('/personal_info')
def view_proffesional(current_user_payload=Depends(get_current_user)):
    
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


@job_seekers_router.put('/personal_info/edit')
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
    

    if not job_seeker_services.check_seeker_exists(job_seeker.username):
        return JSONResponse(status_code=404, content='No seeker found in the system!')
    
    return job_seeker_services.edit_info(job_seeker.username, job_seeker.summary,job_seeker.city,job_seeker.status)

@job_seekers_router.post('/register')
def add_seeker(seeker_username: str = Query(),
              seeker_password: str = Query(),
              seeker_first_name: str = Query(), 
              seeker_last_name: str = Query(),
              seeker_email_adress: str = Query(),
              seeker_city: str = Query(),
              seeker_country: str = Query()):
    
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
    
