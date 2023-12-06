from fastapi import APIRouter, Depends
from common.auth import get_current_user
from services import job_seeker_matching_services
from fastapi import HTTPException

job_seekers_matching_router = APIRouter(prefix='/job_seekers_match', tags=['Seeker Matching Section'])


@job_seekers_matching_router.post('/company', description= 'You can match your cv with a specific Job Ad.')

def match_job_ad(job_ad_id: int, 
                  current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'seekers':
        return HTTPException(status_code=403,
                            detail='Only seekers can send matches')

    seeker_id = current_user_payload.get('id')
    cv_id = job_seeker_matching_services.get_main_cv(seeker_id)
    if not job_seeker_matching_services.check_job_ad_exist(job_ad_id):
        raise HTTPException(status_code=400, detail='No job ad found with this ID')

    if job_seeker_matching_services.check_seeker_status(seeker_id):
        raise HTTPException(status_code=400, detail='You have been already matched')
    
    if job_seeker_matching_services.is_matching_exist(job_ad_id, cv_id):
        raise HTTPException(status_code=400, detail='Already matched')

    return job_seeker_matching_services.match_ad(job_ad_id, cv_id, seeker_id)


@job_seekers_matching_router.get('/pending_list', description= 'You can view pending requests coming from different job ads.')

def view_pending_list(current_user_payload=Depends(get_current_user)):

    if current_user_payload['group'] != 'seekers':
        return HTTPException(status_code=403,
                            detail='Only seekers can view all pending matches')

    seeker_id = current_user_payload.get('id')
    cv_id = job_seeker_matching_services.get_main_cv(seeker_id)
    return job_seeker_matching_services.pending_list(cv_id)


@job_seekers_matching_router.put('/cancel', description= 'You can cancel incoming match requests.')

def cancel_match_request(job_ad_id: int,
                         current_user_payload=Depends(get_current_user)):
    
    if current_user_payload['group'] != 'seekers':
        return HTTPException(status_code=403,
                            detail='Only seekers can send matches')
    
    seeker_id = current_user_payload.get('id')
    cv_id = job_seeker_matching_services.get_main_cv(seeker_id)

    if not job_seeker_matching_services.check_job_ad_exist(job_ad_id):
        raise HTTPException(status_code=400, detail='No job ad found with this ID')
    
    if job_seeker_matching_services.check_if_canceled(job_ad_id, cv_id):
        raise HTTPException(status_code=400, detail='You already canceled this request')
    
    if not job_seeker_matching_services.check_request_exist(job_ad_id, cv_id):
        raise HTTPException(status_code=404, detail='Match request not found!')

    return job_seeker_matching_services.cancel_match(job_ad_id, cv_id)