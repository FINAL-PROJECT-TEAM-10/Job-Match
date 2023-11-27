from fastapi import APIRouter, Query, Depends
from common.auth import get_current_user
from services import job_seeker_matching_services
from fastapi import HTTPException


job_seekers_matching_router = APIRouter(prefix='/job_seekers_match')


@job_seekers_matching_router.post('/company', tags=['Seeker Matching Section'])
def match_company(job_ad_id: int, 
                  current_user_payload=Depends(get_current_user)):

    seeker_id = current_user_payload.get('id') #36
    cv_id = job_seeker_matching_services.get_main_cv(seeker_id)
    if not job_seeker_matching_services.check_job_ad_exist(job_ad_id):
        raise HTTPException(status_code=400, detail='No job ad found with this ID')

    if job_seeker_matching_services.check_seeker_status(seeker_id):
        raise HTTPException(status_code=400, detail='You have been already matched')
    
    if job_seeker_matching_services.is_matching_exist(job_ad_id, cv_id):
        raise HTTPException(status_code=400, detail='Already matched')

    return job_seeker_matching_services.match_ad(job_ad_id, cv_id, seeker_id)
