from data.database import read_query, insert_query, update_query
from fastapi import Response
from fastapi.responses import JSONResponse
from app_models.company_models import Company

def read_companies():
    data = read_query('SELECT * FROM companies')
    return data

def read_company_adress(id: int):
    data = read_query('SELECT * FROM company_contacts WHERE company_id = ?',(id,))
    return data

def read_company_location(location: str):
    data = read_query('SELECT city,country FROM locations WHERE id = ?',(location,))
    return data

def read_company_information(company: str):
    data = read_query('SELECT * FROM companies WHERE id = ?',(company,))
    
    return next((Company.from_company_result(*row) for row in data), None)



