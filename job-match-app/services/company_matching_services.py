from data.database import read_query, insert_query, update_query
from datetime import date,datetime
from fastapi import HTTPException
from mariadb import IntegrityError

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
            
            raise HTTPException(status_code=200, detail=f'Match request sended to cv id : {mini_cv_id}')

    except IntegrityError:
        data = update_query('UPDATE job_ads_has_mini_cvs SET match_status = "Successfull" WHERE job_ad_id = ? AND mini_cv_id = ? AND sender = "Seeker" AND match_status = "Pending"',
                        (job_ad_id, mini_cv_id))
        raise HTTPException(status_code= 200, detail = 'You have already send out a request to the job seeker')

def get_main_cv(seeker_id):

    cv_id = read_query('SELECT id FROM mini_cvs WHERE id = ? AND main_cv = 1', (seeker_id,))

    return bool(cv_id)


def matching_exist(job_ad_id, mini_cv_id):

    check = read_query('SELECT * FROM job_ads_has_mini_cvs WHERE job_ad_id = ? AND mini_cv_id = ? AND match_status = "Pending" AND sender = "Seeker"', (job_ad_id, mini_cv_id))

    return bool(check)