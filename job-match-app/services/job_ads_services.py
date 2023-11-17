from data.database import read_query, insert_query, update_query
from datetime import date,datetime
from app_models.job_ads_models import Job_ad
from fastapi.responses import JSONResponse
from services import job_seeker_services
from mariadb import IntegrityError

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
        ads = [{'Job Description': row[1], 'Minimum Salary': row[2], 'Maximum Salary': row[3], 'Status': row[4], 'Date Posted': row[5]} for row in data]
        return ads
    else:
        return JSONResponse(status_code=404,content='There are no current job ads found')


def get_current_active_job_ads(company_id: int):

    data = read_query('SELECT * FROM job_ads WHERE companies_id = ? AND status = "active"',(company_id,))

    return len(data)

def find_job_ad_by_id(company_id: int, description: str):

    job_ad = read_query('SELECT id FROM job_ads WHERE companies_id = ? AND description = ?', (company_id, description))


    return job_ad[0][0]
