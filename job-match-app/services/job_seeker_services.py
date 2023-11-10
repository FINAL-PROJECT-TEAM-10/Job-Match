from data.database import read_query, insert_query, update_query
from fastapi import Response
from fastapi.responses import JSONResponse
from common.job_seeker_status_check import recognize_status, convert_status
from app_models.job_seeker_models import JobSeekerInfo

def read_seekers():

    data = read_query('SELECT * FROM job_seekers')
    return data

def contacts_info_for_seeker(contact_id: int):

    data = read_query('SELECT email, address, telephone, post_code, locations_id FROM employee_contacts WHERE id = ?', (contact_id,))


    return data

def location_id_from_contacts(contact_id: int):

    data = read_query('SELECT locations_id FROM employee_contacts WHERE id = ?', (contact_id,))

    return data[0][0]

def location_finder(location_id: int):

    data = read_query('SELECT city, country FROM locations WHERE id = ?', (location_id,))

    if data:
        return data
    else:
        return None

def job_seeker_info_username(username: str):

    job_seeker = read_query('SELECT summary, employee_contacts_id, busy FROM job_seekers WHERE username = ?', (username,))
    status = recognize_status(job_seeker[0][2])
    location_id_contacts = location_id_from_contacts(job_seeker[0][1])
    location_seeker = location_finder(location_id_contacts)
    summary = job_seeker[0][0]
    location = location_seeker[0][0]

    return JobSeekerInfo(summary=summary, location=location, status=status)

def check_seeker_exists(username: str):

    check = read_query('SELECT * FROM job_seekers WHERE username = ?', (username,))

    return bool(check)


def edit_info(username: str, summary: str, city: str, status: str):

    converted_status = convert_status(status)
    update_query('UPDATE job_seekers SET summary = ?, busy = ? WHERE username = ?', (summary, converted_status, username))

def get_job_seeker_info(username: str):

    data = read_query('SELECT * FROM job_seekers WHERE username = ?', (username,))

    return data