from data.database import read_query, insert_query, update_query
from datetime import datetime
from fastapi import HTTPException


def match_ad(job_ad_id: int, mini_cv_id: int, seeker_id: int):
    
    if is_matching_exist_pendings(job_ad_id, mini_cv_id):
        update_query('UPDATE job_ads_has_mini_cvs SET match_status = "Successfull" WHERE job_ad_id = ? AND mini_cv_id = ? AND sender = "Company"',
                        (job_ad_id, mini_cv_id))
        
        update_query('UPDATE job_seekers SET busy = 1 WHERE id = ?', (seeker_id,))
        #0 - Active 1- Busy
        raise HTTPException(status_code=200, detail=f'You matched successfully with job ad id: {job_ad_id}')
    else:
        date_matched = datetime.now()
        match_status = 'Pending'
        sender = 'Seeker'
        insert_query('INSERT INTO job_ads_has_mini_cvs (job_ad_id, mini_cv_id, date_matched, match_status, sender) VALUES (?,?,?,?,?)',
                 (job_ad_id, mini_cv_id, date_matched, match_status, sender))
        raise HTTPException(status_code=200, detail=f'Match request sended to job id : {job_ad_id}')

def get_main_cv(seeker_id):

    cv_id = read_query('SELECT id FROM mini_cvs WHERE job_seekers_id = ? AND main_cv = 1', (seeker_id,))

    return cv_id[0][0]


def is_matching_exist(job_ad_id, cv_id):

    check = read_query('SELECT * FROM job_ads_has_mini_cvs WHERE job_ad_id = ? AND mini_cv_id = ? AND match_status = "Pending" AND sender != "Company"', (job_ad_id, cv_id))

    return bool(check)


def check_job_ad_exist(job_ad_id):

    check = read_query('SELECT description FROM job_ads WHERE id = ?', (job_ad_id,))

    return bool(check)

def check_seeker_status(seeker_id):

    check = read_query('SELECT username FROM job_seekers WHERE id = ? AND busy = 1',(seeker_id,))

    return bool(check)


def is_matching_exist_pendings(job_ad_id, cv_id):

    check = read_query('SELECT * FROM job_ads_has_mini_cvs WHERE job_ad_id = ? AND mini_cv_id = ? AND match_status = "Pending" AND sender = "Company"', (job_ad_id, cv_id))

    return bool(check)