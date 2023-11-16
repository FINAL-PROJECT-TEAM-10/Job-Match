from typing import Annotated

from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from app_models.input_models import PasswordUpdater
from common.auth import TokenInfo, get_current_user
from common.mailing import password_reset_email
from services import authorization_services, company_services, job_seeker_services, admin_services

profile_router = APIRouter(prefix='/profile')


@profile_router.get('/info', response_model=TokenInfo,
                    responses={200: {"description": "Informs the user of basic info, which is included in the token."}})
def get_self(current_user_payload=Depends(get_current_user)):
    return JSONResponse(status_code=200,
                        content=current_user_payload)


@profile_router.patch('/password')
def update_password(credentials: PasswordUpdater,
                    current_user_payload=Depends(get_current_user)):
    if authorization_services.is_password_identical_by_type(current_user_payload, credentials.old_password):
        if authorization_services.password_changer(current_user_payload, credentials.new_password):
            return JSONResponse(status_code=200,
                                content='Your password has been changed.')
        else:
            return JSONResponse(status_code=500,
                                content='Could not update password.')
    else:
        return JSONResponse(status_code=403,
                            content='You did not input correctly your current password.')


@profile_router.patch('/password/reset')
def password_reset(username: str, user_type: str):
    mock_payload = {}
    if user_type == 'admins':
        user = admin_services.get_admin(username)
        mock_payload['group'] = 'admins'
    elif user_type == 'companies':
        user = company_services.get_company(username)
        mock_payload['group'] = 'companies'
    elif user_type == 'job_seekers':
        user = job_seeker_services.get_seeker(username)
        mock_payload['group'] = 'job_seekers'
    else:
        return JSONResponse(status_code=400,
                            content='Invalid user type category.'
                                    'Categories can be: admins, companies, job_seekers')

    generated_password = authorization_services.generate_password()
    authorization_services.password_changer(mock_payload, generated_password)

    password_reset_email(user, generated_password)

