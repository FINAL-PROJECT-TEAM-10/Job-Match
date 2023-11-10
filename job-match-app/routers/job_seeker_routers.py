from fastapi import APIRouter, Query, Body,Header, HTTPException
from fastapi.responses import JSONResponse
from services import job_seeker_services

job_seekers_router = APIRouter(prefix='/job_seekers',tags={'Job seekers'})


@job_seekers_router.get('/', description= 'All functions for job seekers')
def get_all_seekers():


    get_seekers = job_seeker_services.read_seekers()

    result = []

    for data in get_seekers:
        seeker_contacts = job_seeker_services.contacts_info_for_seeker(data[10])
        seeker_location = job_seeker_services.location_finder(seeker_contacts[0][4])
        data_dict = {
            "Username": data[1],
            "Email": seeker_contacts [0][0],
            'Adress': seeker_contacts[0][1],
            'Telephone': seeker_contacts[0][2],
            'City': seeker_location[0][0],
            'Post Code': seeker_contacts[0][3],
            'Country': seeker_location[0][1],

        }

        result.append(data_dict)

    return result


@job_seekers_router.get('/personal_info')
def view_proffesional(job_seeker_username: str = Query()):

    if not job_seeker_services.check_seeker_exists(job_seeker_username):
        return JSONResponse(status_code=404, content='No seeker found in the system!')

    current_job_seeker_info = job_seeker_services.job_seeker_info_username(job_seeker_username)

    return current_job_seeker_info


@job_seekers_router.put('/personal_info/edit')
def edit_proffesional_info(job_seeker_username: str = Query(),
                           summary: str = Query(None),
                           city: str = Query(None),
                           status: str =  Query(enum=['Active', 'Busy'])):
    

    if not job_seeker_services.check_seeker_exists(job_seeker_username):
        return JSONResponse(status_code=404, content='No seeker found in the system!')
    
    return job_seeker_services.edit_info(job_seeker_username, summary,city,status)
    