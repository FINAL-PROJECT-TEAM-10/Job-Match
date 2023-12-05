from common import mailing
from data.database import read_query, insert_query, update_query
from datetime import date,datetime
from fastapi import HTTPException
from mariadb import IntegrityError
from services import job_seeker_services

from services.job_ads_services import get_job_ad_as_object

def check_job_ad_exist(job_ad_id):

    check = read_query('SELECT description FROM job_ads WHERE id = ?', (job_ad_id,))

    return bool(check)

def match_cv(job_ad_id: int, mini_cv_id: int):

    try:
        if matching_exist(job_ad_id, mini_cv_id):
            update_query('UPDATE job_ads_has_mini_cvs SET match_status = "Successfull" WHERE job_ad_id = ? AND mini_cv_id = ? AND sender = "Seeker"',
                        (job_ad_id, mini_cv_id))
            update_query('UPDATE job_ads SET status = "archived" WHERE id = ?', (job_ad_id,))

            raise HTTPException(status_code=200, detail=f'You matched successfully with mini cv id: {mini_cv_id}')
        else:

            date_of_match = datetime.now()
            status = 'Pending'
            sender = 'Company'

            insert_query('INSERT INTO job_ads_has_mini_cvs (job_ad_id, mini_cv_id, date_matched, match_status, sender) VALUES (?,?,?,?,?)',
                        (job_ad_id, mini_cv_id, date_of_match, status, sender))

            job_ad = get_job_ad_as_object(job_ad_id)
            mailing.job_seeker_match_request_notification(job_ad, job_ad_id, mini_cv_id)

            raise HTTPException(status_code=200, detail=f'Match request sended to cv id : {mini_cv_id}')

    except IntegrityError:
        data = update_query('UPDATE job_ads_has_mini_cvs SET match_status = "Successfull" WHERE job_ad_id = ? AND mini_cv_id = ? AND sender = "Seeker" AND match_status = "Pending"',
                        (job_ad_id, mini_cv_id))
        raise HTTPException(status_code= 200, detail = 'You have already send out a request to the job seeker')


# TODO: Should be renamed to "is_main_cv"
def get_main_cv(seeker_id):

    cv_id = read_query('SELECT id FROM mini_cvs WHERE id = ? AND main_cv = 1', (seeker_id,))

    return bool(cv_id)

def matching_exist(job_ad_id, mini_cv_id):
    
    check = read_query('SELECT * FROM job_ads_has_mini_cvs WHERE job_ad_id = ? AND mini_cv_id = ? AND match_status = "Pending" AND sender = "Seeker"', 
                       (job_ad_id, mini_cv_id))

    return bool(check)

def pending_cvs(job_ad_id):

    data = read_query('SELECT * FROM job_ads_has_mini_cvs WHERE job_ad_id = ? AND match_status = "Pending" AND sender = "Seeker"', (job_ad_id,))

    if data:
        mini_cv = [{'Mini CV ID': row[1], 'Mini CV Description': mini_cv_description(row[1]), 
                    'Minimal Salary': mini_cv_mini_salary(row[1]), 'Maximum Salary': mini_cv_max_salary(row[1]), 
                    "Preferred Location": job_seeker_services.get_cv_location_name(job_seeker_services.get_cv_location_id(row[1])),
                    'CV created on': mini_cv_date_creation(row[1]),
                    'Date of match request': row[2], 'Status': row[3]
                     } for row in data]
        return mini_cv
    else:
        raise HTTPException(status_code=404, detail='There are no pending matches.')
    

# TODO: These should be mini_cv_id, not job_ad_id
def mini_cv_description(job_ad_id):

     desc = read_query('SELECT description FROM mini_cvs WHERE id = ?', (job_ad_id,))

     return desc[0][0]

def mini_cv_mini_salary(job_ad_id):

     min = read_query('SELECT min_salary FROM mini_cvs WHERE id = ?', (job_ad_id,))

     return min[0][0]

def mini_cv_max_salary(job_ad_id):

     max = read_query('SELECT max_salary FROM mini_cvs WHERE id = ?', (job_ad_id,))

     return max[0][0]

def mini_cv_date_creation(job_ad_id):

     date = read_query('SELECT date_posted FROM mini_cvs WHERE id = ?', (job_ad_id,))

     return date[0][0]


def cancel_request(job_ad_id, mini_cv_id):

    if matching_exist(job_ad_id, mini_cv_id):
       update_query('UPDATE job_ads_has_mini_cvs SET match_status = "Canceled" WHERE job_ad_id = ? AND mini_cv_id = ? AND sender = "Seeker"',
                    (job_ad_id, mini_cv_id))

    # TODO: Consider having this in the if block
    raise HTTPException(status_code=200, detail=f'You canceled the match request for cv with id: {job_ad_id}')
     
def check_if_canceled(job_ad_id, mini_cv_id):

    data = read_query('SELECT * FROM job_ads_has_mini_cvs WHERE job_ad_id = ? AND mini_cv_id = ? AND match_status = "Canceled"',
                      (job_ad_id, mini_cv_id))

    return bool(data)

def check_request_exist(job_ad_id, mini_cv_id):

    data = read_query('SELECT * FROM job_ads_has_mini_cvs WHERE job_ad_id = ? AND mini_cv_id = ?', (job_ad_id, mini_cv_id))

    return bool(data)

def successfull_matches():

    data = read_query('SELECT * FROM job_ads_has_mini_cvs WHERE match_status = "Successfull"')

    if data:
        mini_cv = [{'Mini CV ID': row[1], 'Mini CV Description': mini_cv_description(row[1]), 
                    'Minimal Salary': mini_cv_mini_salary(row[1]), 'Maximum Salary': mini_cv_max_salary(row[1]), 
                    "Preferred Location": job_seeker_services.get_cv_location_name(job_seeker_services.get_cv_location_id(row[1])),
                    'CV created on': mini_cv_date_creation(row[1]),
                    'Date of match request': row[2], 'Status': row[3]
                     } for row in data]
        
        return mini_cv
    
def check_active_cvs(seeker_id):

    cv_id = read_query('SELECT id FROM mini_cvs WHERE id = ?', (seeker_id,))

    return bool(cv_id)