from data.database import read_query, insert_query, update_query
from app_models.job_seeker_models import JobSeekerInfo
from app_models.job_seeker_models import JobSeeker
from app_models.cv_models import CvCreation
from services import admin_services, company_services, job_ads_services , job_seeker_matching_services
from common.country_validators_helpers import find_country_by_city
from common.job_seeker_status_check import recognize_status
from datetime import datetime
from mariadb import IntegrityError
from common.percent_jobad_calculator import *
from common.percent_sections import percent_section_helper, find_names
from common.salary_threshold_calculator_seeker import calculate_salaries
from fastapi import HTTPException


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
    data = read_query('SELECT email, address, telephone, locations_id FROM employee_contacts WHERE id = ?',
                      (contact_id,))

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
    job_seeker = read_query('SELECT summary, employee_contacts_id, busy FROM job_seekers WHERE username = ?',
                            (username,))
    data = read_query('SELECT id FROM job_seekers WHERE username = ?', (username,))

    status = recognize_status(job_seeker[0][2])
    location_id_contacts = location_id_from_contacts(job_seeker[0][1])
    location_seeker = location_finder(location_id_contacts)
    summary = job_seeker[0][0]
    location = location_seeker[0][0]

    if not summary:
        summary = 'No summary'

    return JobSeekerInfo(summary=summary, location=location, status=status, number_of_matches_from_diffrent_cvs=job_seeker_matching_services.find_matched_cvs(data[0][0]))


def check_seeker_exists(username: str):
    check = read_query('SELECT * FROM job_seekers WHERE username = ?', (username,))

    return bool(check)


def seeker_exists_by_id(id):
    return any(read_query('''SELECT id from job_seekers WHERE id = ?''',
                          (id,)))


def find_location_by_city(city: str):
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


def edit_info(username: str, summary: str, city: str):
    update_query('UPDATE job_seekers SET summary = ? WHERE username = ?',
                 (summary,username))

    if not find_location_by_city(city):
        country = find_country_by_city(city)
        insert_query('INSERT INTO locations (city, country) VALUES (?,?)', (city, country))
        contact_id = find_employee_contacts_id(username)
        location_id = find_location_id_by_city_country(city, country)
        update_query('UPDATE employee_contacts SET locations_id = ? WHERE id = ?', (location_id, contact_id))
    else:
        contact_id = find_employee_contacts_id(username)
        location_id = find_location_id_by_city(city)
        update_query('UPDATE employee_contacts SET locations_id = ? WHERE id = ?', (location_id, contact_id))

    raise HTTPException(status_code=200, detail='You successfully edited your personal info')


def get_job_seeker_info(username: str):
    data = read_query('SELECT * FROM job_seekers WHERE username = ?', (username,))

    return data


# TODO: Consider having a more encompassing get function (medium priority)
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


def get_seeker_by_email(email):
    seeker_data = read_query('''
        SELECT js.id, js.username, ec.email, js.first_name, js.last_name, js.summary, js.blocked
        FROM job_seekers as js, employee_contacts as ec
        WHERE js.employee_contacts_id = ec.id AND ec.email = ?
        ''', (email,))

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

    raise HTTPException(status_code=200, detail='Seeker was created')


def check_skill_exist(skill_name: str):
    check = read_query('SELECT * FROM skills_or_requirements WHERE name = ?', (skill_name,))

    return bool(check)


def find_cv_by_seeker_id_description(seeker_id: int, description: str):
    cv_id = read_query('SELECT id FROM mini_cvs WHERE job_seekers_id = ? AND description = ?', (seeker_id, description))

    return cv_id[0][0]


def find_skill_id_by_name(name: str):
    skill_id = read_query('SELECT id FROM skills_or_requirements WHERE name = ?', (name,))

    return skill_id[0][0]

def create_cv(description: str, location: str, remote_location : str,
              min_salary: int, max_salary: int, 
              status: str, job_seeker_id: int, list_skills: list, 
              skill_levels: list, is_main_cv: bool): #['python','js']

    date_posted = datetime.now()
    location_id = read_query('SELECT id FROM locations WHERE city = ?',(location,))

    if location:
        cv_create_id = insert_query('''INSERT INTO mini_cvs (min_salary, max_salary, description, status, date_posted, job_seekers_id, main_cv)
                        VALUES (?,?,?,?,?,?,?)
                      ''', (min_salary, max_salary, description, status, date_posted, job_seeker_id, is_main_cv))
        if remote_location == "No":
            remote_status = False
            specific_location_without_remote = insert_query('INSERT INTO mini_cv_has_locations(mini_cv_id, locations_id, remote_status) VALUES (?,?,?)',
                                             (cv_create_id, location_id[0][0], remote_status,))
        else:
            remote_status = True
            remote_with_specific_location = insert_query('INSERT INTO mini_cv_has_locations(mini_cv_id, locations_id, remote_status) VALUES (?,?,?)',
                                                (cv_create_id, location_id[0][0], remote_status,))
    else:
        if remote_location == "Yes":
           cv_create_id = insert_query('''INSERT INTO mini_cvs (min_salary, max_salary, description, status, date_posted, job_seekers_id, main_cv)
                        VALUES (?,?,?,?,?,?,?)
                      ''', (min_salary, max_salary, description, status, date_posted, job_seeker_id, is_main_cv))
           remote_status = True
           remote_has_specific_location = insert_query('INSERT INTO mini_cv_has_locations(mini_cv_id, remote_status) VALUES (?,?)',
                                                (cv_create_id, remote_status,))
        else:
            raise HTTPException(status_code=404, detail="You have to choose a location. City / Remote or Both ")
    
    cv_id = find_cv_by_seeker_id_description(job_seeker_id, description)
    try:
        for skill, level in zip(list_skills, skill_levels):
            level = int(level)
            if not check_skill_exist(skill):
                raise HTTPException(status_code=404,
                                    detail='''That is not a valid skill name. You can send a ticket suggestion for this skill to our moderation team''')
            else:
                converted_level = convert_level(level)
                skill_id = find_skill_id_by_name(skill)
                insert_query(
                    'INSERT INTO mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (?,?,?)',
                    (cv_id, skill_id, converted_level))
    except IntegrityError:
        raise HTTPException(status_code=400, detail='You are using the same information from your previous CV')
    
    try:

        location_name = company_services.find_location(location_id[0][0])
        location_name = location_name[0][0]

    except IndexError:
        location_name = "No location Set"

    return CvCreation(description=description,location_name=location_name, remote_status=remote_status, min_salary=min_salary, max_salary=max_salary, status=status,
                      date_posted=date_posted)


def view_personal_cvs(seeker_id: int):
    data = read_query('SELECT * FROM mini_cvs WHERE job_seekers_id = ?', (seeker_id,))

    if data:
        ads = [{'Cv ID': row[0], 'Cv Description': row[3], 'Minimum Salary': row[1], 'Maximum Salary': row[2], 
                'Location': get_cv_location_name(get_cv_location_id(row[0])),
                'Status': row[4], 'Date Posted': row[5]} for row in data]
        return ads
    else:
        raise HTTPException(status_code=404, detail='No cvs found!')

def get_cv_location_id(cv_id):

    try:
        cv_location = read_query('SELECT locations_id FROM mini_cv_has_locations WHERE mini_cv_id = ?', (cv_id,))
        cv_location = cv_location[0][0]
    except IndexError:
        cv_location = 0

    return cv_location

def get_cv_location_name(location_id):
    
    try:
        location_name = read_query('SELECT city FROM locations WHERE id = ?', (location_id,))
        location_name = location_name[0][0]
    except IndexError:
        location_name = 'Remote'

    return location_name


def check_owner_cv(cv_id, seeker_id):
    data = read_query('SELECT * FROM mini_cvs WHERE id = ? AND job_seekers_id = ?', (cv_id, seeker_id))

    return bool(data)


def edit_cv(job_seeker_id: int, cv_id: int, min_salary: int, max_salary: int,
            description: str, status, skill_names: list = None, skill_levels: list = None):


    update_query('UPDATE mini_cvs SET min_salary = ?, max_salary = ?, description = ?, status = ? WHERE id = ? AND job_seekers_id = ?',
                 (min_salary, max_salary, description, status, cv_id, job_seeker_id))
    
    if skill_names and skill_levels:
        for skill,level in zip(skill_names, skill_levels):
            if level.isnumeric():
                level = int(level)
                if level > 3:
                    raise HTTPException(status_code=400, detail='Invalid level of skill provided!')
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
    

    raise HTTPException(status_code=200, detail='You successfully edited your selected CV.')


def get_cv_info(seeker_id: int, cv_id: str):
    data = read_query('SELECT * FROM mini_cvs WHERE id = ? AND job_seekers_id = ?', (cv_id, seeker_id))

    return data


def get_all_job_ads():
    data = read_query('SELECT * FROM job_ads WHERE status = "active"')

    if data:
        jb_ads = [{'Company': company_services.find_company_id_byusername_for_job_seeker(row[6]),
                   'Job_Ad Description': row[1], 'Minimum Salary': row[2], 'Maximum Salary': row[3], 
                   "Preferred Location": get_cv_location_name(job_ads_services.get_cv_location_id(row[0])), 'Status': row[4],
                   'Date Posted': row[5]} for row in data]
        return jb_ads
    else:
        raise HTTPException(status_code=404, detail='There is no such company with this job ad')


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

def update_main_cv(cv_id, seeker_id):

    other_cv_id = read_query('SELECT id FROM mini_cvs WHERE main_cv = 1 AND job_seekers_id = ?', (seeker_id,))
    status = ''

    if other_cv_id:
        status = 'Private'
        update_query('UPDATE mini_cvs SET main_cv = 0, status = ?  WHERE id = ? AND job_seekers_id = ?', (status,other_cv_id[0][0], seeker_id))
    status = 'Active'
    update_query('UPDATE mini_cvs SET main_cv = 1, status = ? WHERE id = ? AND job_seekers_id = ?', (status,cv_id, seeker_id))

    raise HTTPException(status_code=200, detail=f'You successfully choose a main CV with id: {cv_id}')

def get_main_cv_id(seeker_id):
    cv_id = read_query('SELECT id FROM mini_cvs WHERE main_cv = 1 AND job_seekers_id = ?', (seeker_id,))

    return cv_id[0][0]

def calculate_percents_job_ad(seeker_id, current_sort, perms, threshold_percent, input_salary = None):

    try:
        cv_id = get_main_cv_id(seeker_id)
    except IndexError:
        raise HTTPException(status_code=404, detail='You have to select a main CV to use this option!')
    
    cv_skills = get_current_cv_skills(cv_id)

    all_job_ads = read_query('SELECT * FROM job_ads')


    if current_sort == 'All':
        my_cv_ad_range = input_salary
        salaries_for_job_ad = calculate_salaries(all_job_ads, threshold_percent)
    
        
    result = []

    for current_job_ad in all_job_ads:
        current_job_requirements = get_current_job_ad_requirements(current_job_ad[0])

        data_dict = {
            current_job_ad[0]: current_job_requirements
        }
        result.append(data_dict)

    filtered_data = {key: value for item in result for key, value in item.items() if value}

    matches_per_job_ad = {}

    for job_ad_id, requirements in filtered_data.items():
        current_percent = percentage_calculator(requirements, cv_skills)
        matches_per_job_ad[job_ad_id] = round(current_percent)

    matched = {}
    for job_ad_id, requirements in filtered_data.items():
        matched[job_ad_id] = find_matched(requirements, cv_skills)
    
    unmatched = {}
    for job_ad_id, requirements in filtered_data.items():
        unmatched[job_ad_id] = find_unmatched(requirements, cv_skills)
    

    if current_sort != 'All':
        return percent_section_helper(current_sort,matches_per_job_ad, perms, matched, unmatched)
    else:
        return filter_by_salaries(my_cv_ad_range,salaries_for_job_ad)


def get_current_job_ad_requirements(job_ad_id:int):
    data = read_query('SELECT skills_or_requirements_id FROM job_ads_has_requirements WHERE job_ads_id = ?', (job_ad_id,))

    #REQUIREMENTS
    result_pairs = [
        f"{get_requirement_name(id)};{get_level(job_ad_id, id)}"
        for job_ad in data
        for id in job_ad
    ]

    return result_pairs

def get_current_cv_skills(cv_id:int):
    cv_skills = read_query('SELECT skills_or_requirements_id FROM mini_cvs_has_skills WHERE mini_cvs_id = ?', (cv_id,))

    #CV SKILLS
    result_pairs = [
        f"{get_requirement_name(id)};{get_level_skill(cv_id, id)}"
        for cv in cv_skills
        for id in cv
    ]

    return result_pairs


def get_requirement_name(id):

    data = read_query('SELECT name FROM skills_or_requirements WHERE id = ?', (id,))

    return data[0][0]

def get_level(job_ad_id, requirement_id):

    data = read_query('SELECT level FROM job_ads_has_requirements WHERE job_ads_id = ? AND skills_or_requirements_id = ?',
                      (job_ad_id,requirement_id))
    
    return data[0][0]

def get_level_skill(cv_id, skill_id):

    data = read_query('SELECT level FROM mini_cvs_has_skills WHERE mini_cvs_id = ? AND skills_or_requirements_id = ?',
                      (cv_id,skill_id))
    
    return data[0][0]

def get_min_salary_and_max(cv_id):

    salary = read_query('SELECT min_salary, max_salary FROM mini_cvs WHERE id = ?', (cv_id,))


    return salary


def filter_by_salaries(current_cv_range, job_ads_calculated_salaries):
    cv_min_salary = current_cv_range[0]
    cv_max_salary = current_cv_range[1]

    result = []
    for current_dict_ad in job_ads_calculated_salaries:
        for key,value in current_dict_ad.items():
            
            min_salary_ad = value[0]
            max_salary_ad = value[1]
            company_id = find_company_id(key)
            description = read_query('SELECT description FROM job_ads WHERE id = ?', (key,))
            original_salary_range_info = original_salary_info(key)

            if cv_min_salary >= min_salary_ad and cv_max_salary <= max_salary_ad:
                    filtered_ads = {
                    'Job AD ID': key,
                    'Company Name': company_services.find_company_id_byusername_for_job_seeker(company_id),
                    'Description': description[0][0],
                    "Prefered Location": get_cv_location_name(job_ads_services.get_cv_location_id(key)),
                    'Original Salary Range':  f'{original_salary_range_info[0][0]} - {original_salary_range_info[0][1]}',
                    'Threshold Salary Range': f'{int(min_salary_ad)} - {int(max_salary_ad)}',
                    }
                    result.append(filtered_ads)

    if not result:
        raise HTTPException(status_code=404, detail="There are no found cv's in this salary search range")
        
    return result


def find_company_id(id):

    data = read_query('SELECT companies_id FROM job_ads WHERE id = ?', (id,))

    return data[0][0]

def is_main_already(cv_id):

    check = read_query('SELECT min_salary FROM mini_cvs WHERE id = ? AND main_cv = 1', (cv_id,))

    return bool(check)

def original_salary_info(job_ad_id: int):

    data = read_query('SELECT min_salary, max_salary FROM job_ads WHERE id = ?', (job_ad_id,))

    return data

def check_is_matched(cv_id):

    check = read_query('SELECT min_salary FROM mini_cvs WHERE id = ? AND status = "Matched" AND main_cv = 1', 
                       (cv_id,))

    return bool(check)

def get_existing_status(cv_id):

    status = read_query('SELECT status FROM mini_cvs WHERE id = ? AND main_cv = 1', (cv_id,))


    return status[0][0]