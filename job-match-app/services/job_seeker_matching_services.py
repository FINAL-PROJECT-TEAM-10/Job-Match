from common import mailing
from data.database import read_query, insert_query, update_query
from datetime import datetime
from fastapi import HTTPException
from mariadb import IntegrityError
from services import job_seeker_services
from services.company_matching_services import get_job_ad_as_object

def match_ad(job_ad_id: int, mini_cv_id: int, seeker_id: int):
    try:
        if is_matching_exist_pendings(job_ad_id, mini_cv_id):
            update_query(
                'UPDATE job_ads_has_mini_cvs SET match_status = "Successfull" WHERE job_ad_id = ? AND mini_cv_id = ? AND sender = "Company"',
                (job_ad_id, mini_cv_id))

            update_query('UPDATE job_seekers SET busy = 1 WHERE id = ?', (seeker_id,))
            
            raise HTTPException(status_code=200, detail=f'You matched successfully with job ad id: {job_ad_id}')
        else:
            date_matched = datetime.now()
            match_status = 'Pending'
            sender = 'Seeker'
            insert_query(
                'INSERT INTO job_ads_has_mini_cvs (job_ad_id, mini_cv_id, date_matched, match_status, sender) VALUES (?,?,?,?,?)',
                (job_ad_id, mini_cv_id, date_matched, match_status, sender))

            cv = job_seeker_services.get_cv_as_object(mini_cv_id)
            job_ad = get_job_ad_as_object(job_ad_id)
            mailing.company_match_request_notification(cv, job_ad, job_ad_id, mini_cv_id)

            raise HTTPException(status_code=200, detail=f'Match request sended to job id : {job_ad_id}')
    except IntegrityError:
        data = update_query(
            'UPDATE job_ads_has_mini_cvs SET match_status = "Successfull" WHERE job_ad_id = ? AND mini_cv_id = ? AND sender = "Company" AND match_status = "Pending"',
            (job_ad_id, mini_cv_id))
        raise HTTPException(status_code=200, detail='You have already send out a request to the company')


def get_main_cv(seeker_id):
    cv_id = read_query('SELECT id FROM mini_cvs WHERE job_seekers_id = ? AND main_cv = 1', (seeker_id,))

    return cv_id[0][0]


def is_matching_exist(job_ad_id, cv_id):
    check = read_query(
        'SELECT * FROM job_ads_has_mini_cvs WHERE job_ad_id = ? AND mini_cv_id = ? AND match_status = "Pending" AND sender != "Company"',
        (job_ad_id, cv_id))

    return bool(check)


def check_job_ad_exist(job_ad_id):
    check = read_query('SELECT description FROM job_ads WHERE id = ?', (job_ad_id,))

    return bool(check)


def check_seeker_status(seeker_id):
    check = read_query('SELECT username FROM job_seekers WHERE id = ? AND busy = 1', (seeker_id,))

    return bool(check)


def is_matching_exist_pendings(job_ad_id, cv_id):
    check = read_query(
        'SELECT * FROM job_ads_has_mini_cvs WHERE job_ad_id = ? AND mini_cv_id = ? AND match_status = "Pending" AND sender = "Company"',
        (job_ad_id, cv_id))

    return bool(check)


def pending_list(cv_id):

    data = read_query('''
                    SELECT ja.id, ja.description, ja.min_salary, ja.max_salary,
                    l.city, ja.date_posted, jamc.date_matched, jamc.match_status, jamc.sender                    
                    FROM job_ads as ja
                    JOIN job_ads_has_locations AS jal ON ja.id = jal.job_ads_id
                    JOIN locations AS l ON l.id = jal.locations_id
                    JOIN job_ads_has_mini_cvs AS jamc ON jamc.mini_cv_id = ja.id
                    WHERE jamc.match_status = "Pending" AND jamc.sender = "Company"
                    AND ja.id = ?''', (cv_id,))


    job_ads = []
    for row in data:
        job_ad_id, description, min_salary, max_salary, city, date_posted, date_matched, match_status, sender = row

        job_ads.append({'Job AD ID': job_ad_id, 'Job AD Description': description,
                        'Minimal Salary': min_salary, 'Maximum Salary': max_salary,
                        "Preferred Location": city,
                        'AD created on': date_posted,
                        'Date of match request': date_matched, 'Status': match_status,
                        'Sender': sender})

    if job_ads:
        return job_ads
    else:
        raise HTTPException(status_code=404, detail='There are no pending matches.')


def cancel_match(job_ad_id, mini_cv_id):
    if is_matching_exist_pendings(job_ad_id, mini_cv_id):
        update_query(
            'UPDATE job_ads_has_mini_cvs SET match_status = "Canceled" WHERE job_ad_id = ? AND mini_cv_id = ? AND sender = "Company"',
            (job_ad_id, mini_cv_id))

        raise HTTPException(status_code=200, detail=f'You canceled the match request for job ad with id: {job_ad_id}')


def check_if_canceled(job_ad_id, mini_cv_id):
    data = read_query(
        'SELECT * FROM job_ads_has_mini_cvs WHERE job_ad_id = ? AND mini_cv_id = ? AND match_status = "Canceled"',
        (job_ad_id, mini_cv_id))

    return bool(data)


def check_request_exist(job_ad_id, mini_cv_id):
    data = read_query('SELECT * FROM job_ads_has_mini_cvs WHERE job_ad_id = ? AND mini_cv_id = ?',
                      (job_ad_id, mini_cv_id))

    return bool(data)


def job_ad_description(job_ad_id):
    desc = read_query('SELECT description FROM job_ads WHERE id = ?', (job_ad_id,))

    return desc[0][0]


def job_min_salary(job_ad_id):
    min = read_query('SELECT min_salary FROM job_ads WHERE id = ?', (job_ad_id,))

    return min[0][0]


def job_max_salary(job_ad_id):
    max = read_query('SELECT max_salary FROM job_ads WHERE id = ?', (job_ad_id,))

    return max[0][0]


def job_date_creation(job_ad_id):
    date = read_query('SELECT date_posted FROM job_ads WHERE id = ?', (job_ad_id,))

    return date[0][0]


def find_matched_cvs(cv_id: int):
    data = read_query('SELECT * FROM mini_cvs WHERE job_seekers_id = ? AND status = "Matched"', (cv_id,))

    return len(data)
