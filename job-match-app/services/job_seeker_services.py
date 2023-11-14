from data.database import read_query, insert_query, update_query
from fastapi.responses import JSONResponse
from common.job_seeker_status_check import recognize_status, convert_status
from app_models.job_seeker_models import JobSeekerInfo
from app_models.job_seeker_models import JobSeeker
from app_models.cv_models import CvCreation
from services import admin_services
from common.country_validators_helpers import find_country_by_city
from datetime import datetime

def read_seekers():

    data = read_query('SELECT * FROM job_seekers')
    return data

def contacts_info_for_seeker(contact_id: int):

    data = read_query('SELECT email, address, telephone, locations_id FROM employee_contacts WHERE id = ?', (contact_id,))


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

    if not summary:
        summary = 'No summary'

    return JobSeekerInfo(summary=summary, location=location, status=status)

def check_seeker_exists(username: str):

    check = read_query('SELECT * FROM job_seekers WHERE username = ?', (username,))

    return bool(check)

def find_location_by_city(city:str):

    data = read_query('SELECT * FROM locations WHERE city = ?', (city,))
    

    if data:
        return data
    else:
        return None

def find_employee_contacts_id(username: str):

    contact_id = read_query('SELECT employee_contacts_id FROM job_seekers WHERE username = ?', (username,))

    return contact_id[0][0]

def find_location_id_by_city_country(city, country):

    location_id = read_query('SELECT id FROM locations WHERE city = ? AND country = ?', (city, country))

    return location_id[0][0]

def find_location_id_by_city(city):

    location_id = read_query('SELECT id FROM locations WHERE city = ?', (city,))

    return location_id[0][0]

def edit_info(username: str, summary: str, city: str, status: str):

    converted_status = convert_status(status)
    update_query('UPDATE job_seekers SET summary = ?, busy = ? WHERE username = ?', (summary, converted_status, username))

    if not find_location_by_city(city):
        country = find_country_by_city(city)
        insert_query('INSERT INTO locations (city, country) VALUES (?,?)', (city,country))
        contact_id = find_employee_contacts_id(username)
        location_id = find_location_id_by_city_country(city, country)
        update_query('UPDATE employee_contacts SET locations_id = ? WHERE id = ?', (location_id,contact_id))
    else:
        contact_id = find_employee_contacts_id(username)
        location_id = find_location_id_by_city(city)
        update_query('UPDATE employee_contacts SET locations_id = ? WHERE id = ?', (location_id, contact_id))

    return JSONResponse(status_code=200, content='You successfully edited your personal info')

def get_job_seeker_info(username: str):

    data = read_query('SELECT * FROM job_seekers WHERE username = ?', (username,))

    return data


# TODO: Consider having a more encompassing get function
def get_seeker(username) -> None | JobSeeker:
    seeker_data = read_query('''
        SELECT js.id, js.username, ec.email, js.first_name, js.last_name, js.summary, js.blocked
        FROM job_seekers as js, employee_contacts as ec
        WHERE js.employee_contacts_id = ec.id AND js.username = ?
        ''', (username,))

    return next((JobSeeker.from_query_results(*row) for row in seeker_data), None)


def create_seeker(username, password, first_name, last_name, email, city, country):
    from services.authorization_services import get_password_hash

    location_id = admin_services.find_location_id(city, country)

    if not location_id:
        location_id = admin_services.create_location(city, country)

    password = get_password_hash(password)
    adress = ' '
    telephone = ' '
    busy = False
    blocked = False
    approved = 0

    new_contact = insert_query('''
    INSERT INTO employee_contacts
    (email, address, telephone,locations_id)
    VALUES (?,?,?,?)
''', (email, adress, telephone, location_id)
    )

    new_seeker = insert_query('''
    INSERT INTO job_seekers
    (username, password, first_name, last_name, busy, blocked, approved, employee_contacts_id)
    VALUES (?,?,?,?,?,?,?,?)
    ''', (username, password, first_name, last_name, busy, blocked, approved, new_contact)
                              )
    
    return JSONResponse(status_code=200, content='Seeker was created')


def create_cv(description: str, min_salary: int, max_salary: int, status: str, job_seeker_id: int):

    date_posted = datetime.now()

    cv = insert_query('''INSERT INTO mini_cvs (min_salary, max_salary, description, status, date_posted, job_seekers_id)
                        VALUES (?,?,?,?,?,?)
                      ''', (min_salary, max_salary, description, status, date_posted, job_seeker_id))
    

    return CvCreation(description=description, min_salary=min_salary, max_salary=max_salary,status=status, date_posted=date_posted)


def view_personal_cvs(seeker_id:int ):

    data = read_query('SELECT * FROM mini_cvs WHERE job_seekers_id = ?', (seeker_id,))

    if data:
        ads = [{'Cv Description': row[3], 'Minimum Salary': row[1], 'Maximum Salary': row[2], 'Status': row[4], 'Date Posted': row[5]} for row in data]
        return ads
    else:
        return JSONResponse(status_code=404, content='No cvs found!')