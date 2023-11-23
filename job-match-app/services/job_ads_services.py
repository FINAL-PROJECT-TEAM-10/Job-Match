from data.database import read_query, insert_query, update_query
from datetime import date,datetime
from app_models.job_ads_models import Job_ad
from fastapi.responses import JSONResponse
from services import job_seeker_services
from mariadb import IntegrityError
from common.percantage_cv_calculator import cv_percentage_calculator
from common.percent_section_cv import percent_section_helper

def find_company(name_of_company):
    
    data = read_query('SELECT id FROM companies WHERE username = ?',(name_of_company,))
    return data

def find_name_by_id(id: int):
    data = read_query('SELECT username from companies WHERE id = ?',(id,))
    return data[0][0]

def create_job_add(description: str, min_salary: int, max_salary: int, status: str,company_id: int, requirements_names: list, requirements_levels: list) -> Job_ad:

    date_posted = datetime.now()
    
    create_job = insert_query('INSERT INTO job_ads(description,min_salary,max_salary,status,date_posted,companies_id) VALUES (?,?,?,?,?,?)', 
                              (description,min_salary,max_salary,status,date_posted,company_id,))
    
    job_ad_id = find_job_ad_by_id(company_id, description)

    try:
        for requirement,levels in zip(requirements_names, requirements_levels):
            levels = int(levels)
            if not job_seeker_services.check_skill_exist(requirement):
                return JSONResponse(status_code=404,content='That is not a valid requirement name. You can send a ticker suggestion for this requirement to our moderation team')
            else:
                requirement_level_convertor = job_seeker_services.convert_level(levels)
                requirement_id = job_seeker_services.find_skill_id_by_name(requirement)
                insert_query('INSERT INTO job_ads_has_requirements (job_ads_id,skills_or_requirements_id,level) VALUES (?,?,?)',
                            (job_ad_id, requirement_id, requirement_level_convertor))
    except IntegrityError:
        return JSONResponse(status_code=404,content="Duplicating description or requirements")

    return Job_ad(description=description, min_salary=min_salary, max_salary=max_salary, date_posted=date_posted, status = status)



def check_company_exist(name: str):
    data = read_query('SELECT username FROM companies WHERE username = ?',(name,))
    return bool(data)

def view_all_job_ads(username: str):
    company_id = find_company(username)
    data = read_query('SELECT * FROM job_ads WHERE companies_id = ?',(company_id[0][0],))
    return data

def view_job_ads_by_id(ads_id: int):

    data = read_query('SELECT * FROM job_ads WHERE companies_id = ?', (ads_id,))

    if data:
        ads = [{'Job Ad ID': row[0],'Job Description': row[1], 'Minimum Salary': row[2], 'Maximum Salary': row[3], 'Status': row[4], 'Date Posted': row[5]} for row in data]
        return ads
    else:
        return JSONResponse(status_code=404,content='There are no current job ads found')


def get_current_active_job_ads(company_id: int):

    data = read_query('SELECT * FROM job_ads WHERE companies_id = ? AND status = "active"',(company_id,))

    return len(data)

def find_job_ad_by_id(company_id: int, description: str):

    job_ad = read_query('SELECT id FROM job_ads WHERE companies_id = ? AND description = ?', (company_id, description))


    return job_ad[0][0]

def check_owner_company(job_ad_id, company_id):

    data = read_query('SELECT * FROM job_ads WHERE id = ? AND companies_id = ?', (job_ad_id, company_id,))

    return bool(data)


def check_company_information(job_ad_id: int, company_id: str):

    data = read_query('SELECT * FROM job_ads WHERE id = ? AND companies_id = ?', (job_ad_id, company_id,))

    return data

def edit_job_ads(company_id:int, job_ads_id: int, min_salary: int, max_salary: int, 
            description: str, requirement_names: list, requirement_levels: list):


    update_query('UPDATE job_ads SET min_salary = ?, max_salary = ?, description = ? WHERE id = ? AND companies_id = ?',
                 (min_salary, max_salary, description, job_ads_id, company_id))
    
    if requirement_names and requirement_levels:
        for requirement,level in zip(requirement_names, requirement_levels):

            if level.isnumeric():
                level = int(level)
                converted_level = job_seeker_services.convert_level(level)

            else:
                level_num = convert_level_name(level)
                converted_level = level_num

            requirements_id = find_requirement_by_name(requirement)

            if not check_requirement_ad_exist(job_ads_id, requirements_id):
                insert_query('INSERT INTO job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (?,?,?)',
                            (job_ads_id, requirements_id, converted_level))
                
            else:
                try:
                    update_query('UPDATE job_ads_has_requirements SET skills_or_requirements_id = ?, level = ? WHERE job_ads_id = ?', 
                                (requirements_id, converted_level, job_ads_id))
                except IntegrityError:
                        update_query('UPDATE job_ads_has_requirements SET level = ? WHERE job_ads_id = ? AND skills_or_requirements_id = ?',    
                                (converted_level, job_ads_id, requirements_id))


    return JSONResponse(status_code=200, content='You successfully edited your selected Job AD.')

def existing_requirements(job_ad_id: int):

    all_requirements = read_query('SELECT skills_or_requirements_id FROM job_ads_has_requirements WHERE job_ads_id = ?', (job_ad_id,))

    return all_requirements

def find_requirement_by_id(job_ad_id: int):

    name = read_query('SELECT name FROM skills_or_requirements WHERE id = ?', (job_ad_id,))

    return name[0][0]

def find_requirements_level(job_ad_id, requirement_id):

    level = read_query('SELECT level FROM job_ads_has_requirements WHERE job_ads_id = ? AND skills_or_requirements_id = ?', (job_ad_id,requirement_id))

    return level[0][0]

def find_requirement_by_name(skill_name: int):

    skill_id = read_query('SELECT id FROM skills_or_requirements WHERE name = ?', (skill_name,))

    return skill_id[0][0]

def check_requirement_ad_exist(job_ad_id, requirement_id):

    data = read_query('SELECT * FROM job_ads_has_requirements WHERE job_ads_id = ? AND skills_or_requirements_id = ?',
                      (job_ad_id, requirement_id))
    
    return bool(data)

def convert_level_name(level):
    result = ''
    if level == 'Beginner':
        result = 1
    elif level == 'Intermidiate':
        result = 2
    elif level == 'Advanced':
        result = 3

    return int(result)


def get_level_job_ad(job_ad_id: int, requirement_id: int):
    data = read_query('SELECT level FROM job_ads_has_requirements WHERE job_ads_id = ? AND skills_or_requirements_id = ?', (job_ad_id, requirement_id,))

    return data[0][0]


def get_current_job_ad(job_ads_id:int):
    job_ad = read_query('SELECT skills_or_requirements_id FROM job_ads_has_requirements WHERE job_ads_id = ?', (job_ads_id,))

    result_pairs = [
        f"{get_skill_name(id)};{get_level_job_ad(job_ads_id, id)}"
        for ad in job_ad
        for id in ad
    ]

    return result_pairs


def calculate_percantage_cv(job_ad_id, sorting, perms):

    ads = read_query('SELECT skills_or_requirements_id FROM job_ads_has_requirements WHERE job_ads_id = ?', (job_ad_id,))

    get_main_cv = read_query('SELECT * FROM mini_cvs WHERE main_cv = 1')

    current_job_ad = get_current_job_ad(job_ad_id)

    result = []

    for current_mini_cv in get_main_cv:
        current_cv_skills = get_main_cv_skills(current_mini_cv[0])

        data_dict = {
           current_mini_cv[0]: current_cv_skills
        }
        result.append(data_dict)
    
    filtered_data = {key: value for item in result for key, value in item.items() if value}

    matches_per_cv = {}

    for cv_id, requirements in filtered_data.items():
        current_percent = cv_percentage_calculator(current_job_ad, requirements)
        matches_per_cv[cv_id] = round(current_percent)

    #TODO : SALARY CALCULATION NEED
    
    return percent_section_helper(sorting,matches_per_cv,perms)


def get_skill_name(id):

    data = read_query('SELECT name FROM skills_or_requirements WHERE id = ?', (id,))

    return data[0][0]

def get_level(mini_cv_id,skill_id):

    data = read_query('SELECT level FROM mini_cvs_has_skills WHERE mini_cvs_id = ? AND skills_or_requirements_id = ? ',
                      (mini_cv_id,skill_id,))

    return data[0][0]

def get_main_cv_skills(mini_cv_id:int):
    data = read_query('SELECT skills_or_requirements_id FROM mini_cvs_has_skills WHERE mini_cvs_id = ?', (mini_cv_id,))

    result_pairs = [
        f"{get_skill_name(id)};{get_level(mini_cv_id, id)}"
        for job_ad in data
        for id in job_ad
    ]

    return result_pairs


