from data.database import read_query, insert_query, update_query
from datetime import date
from app_models.job_ads_models import Job_ad

def find_company(name_of_company):
    
    data = read_query('SELECT id FROM companies WHERE username = ?',(name_of_company,))
    return data

def find_name_by_id(id: int):
    data = read_query('SELECT username from companies WHERE id = ?',(id,))
    return data[0][0]

def create_job_add(description: str, min_salary: int, max_salary: int, status: str, date_posted: date, name_of_company: str) -> Job_ad:

    get_company = find_company(name_of_company)
    the_company_name = find_name_by_id(get_company[0][0])
    
    create_job = insert_query('INSERT INTO job_ads(description,min_salary,max_salary,status,date_posted,companies_id) VALUES (?,?,?,?,?,?)', 
                              (description,min_salary,max_salary,status,date_posted,get_company[0][0],))
    
    return Job_ad(description=description, min_salary=min_salary, max_salary=max_salary, date_posted=date_posted, status = status, name_of_company = the_company_name)

def check_company_exist(name: str):
    data = read_query('SELECT username FROM companies WHERE username = ?',(name,))
    return bool(data)

def view_all_job_ads(username: str):
    company_id = find_company(username)
    data = read_query('SELECT * FROM job_ads WHERE companies_id = ?',(company_id[0][0],))
    return data
