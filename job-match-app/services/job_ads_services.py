from data.database import read_query, insert_query, update_query
from datetime import date,datetime
from app_models.job_ads_models import Job_ad
from fastapi.responses import JSONResponse

def find_company(name_of_company):
    
    data = read_query('SELECT id FROM companies WHERE username = ?',(name_of_company,))
    return data

def find_name_by_id(id: int):
    data = read_query('SELECT username from companies WHERE id = ?',(id,))
    return data[0][0]

def create_job_add(description: str, min_salary: int, max_salary: int, status: str,company_id: int) -> Job_ad:

    date_posted = datetime.now()
    
    create_job = insert_query('INSERT INTO job_ads(description,min_salary,max_salary,status,date_posted,companies_id) VALUES (?,?,?,?,?,?)', 
                              (description,min_salary,max_salary,status,date_posted,company_id,))
    
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
