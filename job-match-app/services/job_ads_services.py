from data.database import read_query, insert_query, update_query
from datetime import date
from app_models.job_ads_models import Job_ad

def find_company(name_of_company):
    data = read_query('SELECT id FROM companies WHERE username = ?',(name_of_company,))
    return data


def create_job_add(description: str, min_salary: int, max_salary: int, status: str, date_posted: date, name_of_company: str) -> Job_ad:

    get_company = find_company(name_of_company)
    the_company_name = get_company[0][0]
    
    create_job = insert_query('INSERT INTO job_ads(description,min_salary,max_salary,status,date_posted,companies_id) VALUES (?,?,?,?,?,?)', 
                              (description,min_salary,max_salary,status,date_posted,the_company_name,))
    
    return Job_ad(description=description, min_salary=min_salary, max_salary=max_salary, date_posted=date_posted, status = status)