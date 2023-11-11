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

# TODO: The get below doesn't consider multiple addresses for a company!!!
#  Consider having a main column to get a company's main address
def get_company(username) -> None | Company:
    company_data = read_query('''
        SELECT c.id, c.username, cc.email, cc.address, cc.telephone, l.country, l.city, c.blocked
        FROM companies as c, company_contacts as cc, locations as l
        WHERE c.username = ? AND cc.company_id = c.id AND cc.locations_id = l.id
        ''', (username,))

    return next((Company.from_query_result(*row) for row in company_data), None)
