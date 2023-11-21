from data.database import read_query, insert_query, update_query
from fastapi import Response
from fastapi.responses import JSONResponse
from app_models.company_models import Company
from services import admin_services
from services.authorization_services import get_password_hash
from common.country_validators_helpers import *
from services import job_seeker_services


def read_companies():
    data = read_query('SELECT * FROM companies')
    return data


def read_company_adress(id: int):
    data = read_query('SELECT * FROM company_contacts WHERE company_id = ?', (id,))
    return data


def read_company_location(location_id: int):
    data = read_query('SELECT city,country FROM locations WHERE id = ?', (location_id,))
    return data


def read_company_information(company: str):
    data = read_query('SELECT * FROM companies WHERE id = ?', (company,))

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


def get_company_by_email(email):
    company_data = read_query('''
        SELECT c.id, c.username, cc.email, cc.address, cc.telephone, l.country, l.city, c.blocked
        FROM companies as c, company_contacts as cc, locations as l
        WHERE cc.email = ? AND cc.company_id = c.id AND cc.locations_id = l.id
        ''', (email,))

    return next((Company.from_query_result(*row) for row in company_data), None)


def check_company_exist(name: str):
    data = read_query('SELECT username FROM companies WHERE username = ?', (name,))
    return bool(data)


def find_company_id_byusername(nickname: str):
    data = read_query('SELECT id FROM companies WHERE username = ?', (nickname,))
    return data[0][0]


def create_company(Company_Name, Password, Company_City, Company_Country, Company_Adress, Telephone_Number,
                   Email_Adress):
    location_id = admin_services.find_location_id(Company_City, Company_Country)

    if not location_id:
        location_id = admin_services.create_location(Company_City, Company_Country)

    password = get_password_hash(Password)

    create_new_company = insert_query('''
        INSERT INTO companies
        (username,password)
        VALUES (?,?)
        ''', (Company_Name, password,))

    company_id = find_company_id_byusername(Company_Name)

    create_new_company_contact = insert_query('''
    INSERT INTO company_contacts
    (email, address, telephone, locations_id,company_id)
    VALUES (?,?,?,?,?)
    ''', (Email_Adress, Company_Adress, Telephone_Number, location_id, company_id,))

    return JSONResponse(status_code=200, content='Your company has been created')


def location_id(contact_id: int):
    data = read_query('SELECT locations_id FROM company_contacts WHERE company_id = ?', (contact_id,))

    return data[0][0]


def find_location(location_id: int):
    data = read_query('SELECT city, country FROM locations WHERE id = ?', (location_id,))

    if data:
        return data
    else:
        return None


def get_company_info_name(company_name: str):
    company = read_query('SELECT username,description FROM companies WHERE username = ?', (company_name,))

    return company


def everything_from_companies_by_username(username: str):
    company = read_query('SELECT * FROM companies WHERE username = ?', (username,))

    return company


def edit_company_information(username: str, description: str, city: str, address: str, telephone: int):
    company_id = find_company_id_byusername(username)

    update_query('UPDATE companies SET description = ? WHERE username = ?', (description, username,))
    update_query('UPDATE company_contacts SET address = ?, telephone = ? WHERE company_id = ?',
                 (address, telephone, company_id,))

    if not job_seeker_services.find_location_by_city(city):
        country = find_country_by_city(city)
        insert_query('INSERT INTO locations(city,country) VALUES (?,?)', (city, country,))
        location_id = job_seeker_services.find_location_id_by_city_country(city, country)
        update_query('UPDATE company_contacts SET locations_id = ? WHERE company_id = ?', (location_id, company_id,))
    else:
        location_id = job_seeker_services.find_location_id_by_city(city)
        update_query('UPDATE company_contacts SET locations_id = ? WHERE company_id = ?', (location_id, company_id,))

    return JSONResponse(status_code=200, content="You successfully edited your personal company information")

def find_company_id_byusername_for_job_seeker(id: int):
    data = read_query('SELECT username FROM companies WHERE id = ?',(id,))
    return data[0][0]

def view_all_cvs():

    data = read_query('SELECT * FROM mini_cvs WHERE status = "Active"')

    if data:
        ads = [{'CV Creator': job_seeker_services.get_username_by_id(row[6]), 'Cv Description': row[3], 'Minimum Salary': row[1], 'Maximum Salary': row[2], 'Status': row[4], 'Date Posted': row[5]} for row in data]
        return ads
    else:
        return JSONResponse(status_code=404, content='No cvs found!')
