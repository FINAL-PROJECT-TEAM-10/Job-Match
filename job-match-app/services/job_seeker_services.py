from data.database import read_query, insert_query, update_query
from fastapi.responses import JSONResponse
from common.job_seeker_status_check import recognize_status, convert_status
from app_models.job_seeker_models import JobSeekerInfo
from app_models.job_seeker_models import JobSeeker
from app_models.cv_models import CvCreation
from services import admin_services,company_services
from common.country_validators_helpers import find_country_by_city
from datetime import datetime
from mariadb import IntegrityError


def convert_level(level):
    result = ''
    if level == 1:
        result = 'Beginner'
    elif level == 2:
        result = 'Intermidiate'
    elif level == 3:
        result = 'Advanced'

    return result

def convert_level_name(level):
    result = ''
    if level == 'Beginner':
        result = 1
    elif level == 'Intermidiate':
        result = 2
    elif level == 'Advanced':
        result = 3

    return int(result)

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

def get_username_by_id(seeker_id: int):

    username = read_query('SELECT username FROM job_seekers WHERE id = ?', (seeker_id,))

    return username[0][0]


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

def check_skill_exist(skill_name: str):

    check = read_query('SELECT * FROM skills_or_requirements WHERE name = ?', (skill_name,))

    return bool(check)

def find_cv_by_seeker_id_description(seeker_id: int, description: str):

    cv_id = read_query('SELECT id FROM mini_cvs WHERE job_seekers_id = ? AND description = ?', (seeker_id, description))


    return cv_id[0][0]

def find_skill_id_by_name(name:str):

    skill_id = read_query('SELECT id FROM skills_or_requirements WHERE name = ?', (name,))

    return skill_id[0][0]

def create_cv(description: str, min_salary: int, max_salary: int, 
              status: str, job_seeker_id: int, list_skills: list, 
              skill_levels: list, is_main_cv: bool): #['python','js']

    date_posted = datetime.now()

    cv = insert_query('''INSERT INTO mini_cvs (min_salary, max_salary, description, status, date_posted, job_seekers_id, main_cv)
                        VALUES (?,?,?,?,?,?)
                      ''', (min_salary, max_salary, description, status, date_posted, job_seeker_id, is_main_cv))
    
    cv_id = find_cv_by_seeker_id_description(job_seeker_id, description)
    try:
        for skill,level in zip(list_skills, skill_levels):
            level = int(level)
            if not check_skill_exist(skill):
                return JSONResponse(status_code=404, detail='''That is not a valid skill name. You can send a ticket suggestion for this skill to our moderation team''')
            else:
                converted_level = convert_level(level)
                skill_id = find_skill_id_by_name(skill)
                insert_query('INSERT INTO mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (?,?,?)',
                            (cv_id, skill_id, converted_level))
    except IntegrityError:
        return JSONResponse(status_code=400, content='You are using the same information from your previous CV')
    

    return CvCreation(description=description, min_salary=min_salary, max_salary=max_salary,status=status, date_posted=date_posted)


def view_personal_cvs(seeker_id:int ):

    data = read_query('SELECT * FROM mini_cvs WHERE job_seekers_id = ?', (seeker_id,))

    if data:
        ads = [{'Cv ID': row[0], 'Cv Description': row[3], 'Minimum Salary': row[1], 'Maximum Salary': row[2], 'Status': row[4], 'Date Posted': row[5]} for row in data]
        return ads
    else:
        return JSONResponse(status_code=404, content='No cvs found!')

def get_all_requirements():

    ...


def check_owner_cv(cv_id, seeker_id):

    data = read_query('SELECT * FROM mini_cvs WHERE id = ? AND job_seekers_id = ?', (cv_id,seeker_id))

    return bool(data)


def edit_cv(job_seeker_id:int, cv_id: int, min_salary: int, max_salary: int, 
            description: str, status, skill_names: list = None, skill_levels: list = None):


    update_query('UPDATE mini_cvs SET min_salary = ?, max_salary = ?, description = ?, status = ? WHERE id = ? AND job_seekers_id = ?',
                 (min_salary, max_salary, description, status, cv_id, job_seeker_id))
    
    if skill_names and skill_levels:
        for skill,level in zip(skill_names, skill_levels):
            if level.isnumeric():
                level = int(level)
                converted_level = convert_level(level)
            else:
                level_num = convert_level_name(level)
                converted_level = level_num
            skill_id = find_skill_id_by_name(skill)
            if not check_skill_cv_exist(cv_id, skill_id):
                insert_query('INSERT INTO mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (?,?,?)',
                            (cv_id, skill_id, converted_level))
            else:
                try:
                    update_query('UPDATE mini_cvs_has_skills SET skills_or_requirements_id = ?, level = ? WHERE mini_cvs_id = ?', 
                                (skill_id, converted_level, cv_id))
                except IntegrityError:
                        update_query('UPDATE mini_cvs_has_skills SET level = ? WHERE mini_cvs_id = ? AND skills_or_requirements_id = ?',    
                                (converted_level, cv_id, skill_id))
    

    return JSONResponse(status_code=200, content='You successfully edited your selected CV.')

def get_cv_info(seeker_id: int, cv_id: str):

    data = read_query('SELECT * FROM mini_cvs WHERE id = ? AND job_seekers_id = ?', (cv_id, seeker_id))

    return data

def get_all_job_ads():

    data = read_query('SELECT * FROM job_ads WHERE status = "active"')

    if data:
        jb_ads = [{'Company': company_services.find_company_id_byusername_for_job_seeker(row[6]), 'Job_Ad Description': row[1], 'Minimum Salary': row[2], 'Maximum Salary': row[3], 'Status': row[4], 'Date Posted': row[5]} for row in data]
        return jb_ads
    else:
        return JSONResponse(status_code=404, content='There is no such company with this job ad')


def get_existing_skills(cv_id: int):

    all_skills = read_query('SELECT skills_or_requirements_id FROM mini_cvs_has_skills WHERE mini_cvs_id = ?', (cv_id,))

    return all_skills

def find_skill_name_by_id(skill_id: int):

    name = read_query('SELECT name FROM skills_or_requirements WHERE id = ?', (skill_id,))

    return name[0][0]

def find_level_by_ids(cv_id, skill_id):

    level = read_query('SELECT level FROM mini_cvs_has_skills WHERE mini_cvs_id = ? AND skills_or_requirements_id = ?', (cv_id,skill_id))

    return level[0][0]


def find_skill_id_by_name(skill_name: int):

    skill_id = read_query('SELECT id FROM skills_or_requirements WHERE name = ?', (skill_name,))

    return skill_id[0][0]

def check_skill_cv_exist(cv_id, skill_id):

    data = read_query('SELECT * FROM mini_cvs_has_skills WHERE mini_cvs_id = ? AND skills_or_requirements_id = ?',
                      (cv_id, skill_id))

    return bool(data)