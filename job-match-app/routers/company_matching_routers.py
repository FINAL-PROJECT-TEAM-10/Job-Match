from fastapi import APIRouter, Query,Depends,Form , HTTPException
from common.auth import get_current_user

companies_matching_router = APIRouter(prefix= '/companies_match')

@companies_matching_router.post('/', tags=['Company Job Ads Matching Section'])

def view_all_companies(current_user_payload=Depends(get_current_user)):
    if current_user_payload['group'] != 'companies':
        return HTTPException(status_code=403,
                            detail= 'This option is only available for Companies')