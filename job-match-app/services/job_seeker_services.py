from data.database import read_query, insert_query, update_query
from fastapi import Response
from fastapi.responses import JSONResponse


def read_seekers():

    data = read_query('SELECT * FROM job_seekers')
    return data

def contacts_info_for_seeker(contact_id: int):

    data = read_query('SELECT email, address, telephone, post_code, locations_id FROM employee_contacts WHERE id = ?', (contact_id,))


    return data

def location_finder(location_id: int):

    data = read_query('SELECT city, country FROM locations WHERE id = ?', (location_id,))

    return data