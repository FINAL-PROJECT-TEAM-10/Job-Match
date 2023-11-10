from data.database import read_query, insert_query, update_query
from fastapi import Response
from fastapi.responses import JSONResponse

def read_companies():
    data = read_query('SELECT * FROM companies')
    return data

def read_company_adress(id: int):
    data = read_query('SELECT * FROM company_contacts WHERE company_id = ?',(id,))
    return data

def read_company_country(id: int):
    data = read_query('')
