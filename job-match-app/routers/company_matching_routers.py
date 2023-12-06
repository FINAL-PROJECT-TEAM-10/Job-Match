from fastapi import APIRouter, Depends, HTTPException
from common.auth import get_current_user
from services import company_matching_services

companies_matching_router = APIRouter(prefix= '/companies_match')


@companies_matching_router.post('/', description= 'You can match a Cv using your specific Job Ad Id.', 
                                tags=['Company Job Ads Searching/Matching Section'])

def match_job_seeker(job_ad_id: int, mini_cv_id: int, current_user_payload = Depends(get_current_user)):

    if current_user_payload['group'] != 'companies':
        return HTTPException(status_code=403,
                            detail= 'This option is only available for Companies')
    
    if not company_matching_services.check_job_ad_exist(job_ad_id):
        raise HTTPException(status_code = 404, detail= 'That is not a valid id for your job ads')
    
    if not company_matching_services.get_main_cv(mini_cv_id):
        raise HTTPException(status_code = 404, detail= 'That is not a valid id for job seeker cv')

    return company_matching_services.match_cv(job_ad_id, mini_cv_id)
    

@companies_matching_router.get('/requests', description= 'You can view all pending match requests using your Job Ad Id.', 
                               tags=['Company Job Ads Searching/Matching Section'])

def view_all_pending_match_requests(job_ad_id: int, current_user_payload = Depends(get_current_user)):

    if current_user_payload['group'] != 'companies':
        return HTTPException(status_code=403,
                            detail= 'This option is only available for Companies')
    
    if not company_matching_services.check_job_ad_exist(job_ad_id):
        raise HTTPException(status_code = 404, detail= 'That is not a valid id for your job ads')
    
    return company_matching_services.pending_cvs(job_ad_id)


@companies_matching_router.put('/cancel', description= 'You can cancel a specific match request using your Job Ad Id.', 
                               tags= ['Company Job Ads Searching/Matching Section'])

def cancel_a_request(job_ad_id: int, mini_cv_id: int, current_user_payload = Depends(get_current_user)):

    if current_user_payload['group'] != 'companies':
        return HTTPException(status_code=403,
                            detail= 'This option is only available for Companies')
    
    if not company_matching_services.check_job_ad_exist(job_ad_id):
        raise HTTPException(status_code = 404, detail= 'That is not a valid id for your job ads')
    
    if not company_matching_services.check_active_cvs(mini_cv_id):
        raise HTTPException(status_code = 404, detail= 'That is not a valid id for job seeker cv')
    
    if not company_matching_services.check_request_exist(job_ad_id,mini_cv_id):
        raise HTTPException(status_code = 404, detail= 'There is no request to cancel')
    
    if company_matching_services.check_if_canceled(job_ad_id, mini_cv_id):
        raise HTTPException(status_code=400, detail='You already canceled this request')
    
    return company_matching_services.cancel_request(job_ad_id, mini_cv_id)

@companies_matching_router.get('/requests/matched', description= 'You can view all successfull matches using your Job Ad Id.', 
                               tags=['Company Job Ads Searching/Matching Section'])

def view_all_successfull_matches(current_user_payload = Depends(get_current_user)):

    if current_user_payload['group'] != 'companies':
        return HTTPException(status_code=403,
                            detail= 'This option is only available for Companies')

    return company_matching_services.successfull_matches()