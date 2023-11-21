from time import time
from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends, Body, Query
from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError

from app_models.input_models import PasswordUpdater
from app_models.token_models import ActivationData
from common.auth import TokenInfo, get_current_user
from common.mailing import password_reset_email, password_reset_activation_email
from services import authorization_services, company_services, job_seeker_services, admin_services

profile_router = APIRouter(prefix='/profile', tags={'Profile info and password management'})


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


@profile_router.patch('/password/forgotten')
def forgotten_password_activation_link(email: str, user_type: str):
    fake_payload = {}
    if user_type == 'admins':
        user = admin_services.get_admin_by_email(email)
    elif user_type == 'companies':
        user = company_services.get_company_by_email(email)
    elif user_type == 'job_seekers':
        user = job_seeker_services.get_seeker_by_email(email)
    else:
        return JSONResponse(status_code=400,
                            content='Invalid user type category.'
                                    'Categories can be: admins, companies, job_seekers')

    if user:
        activation_data = ActivationData(id=user.id,
                                         email=user.email,
                                         username=user.username,
                                         group=user.group,
                                         purpose='forgotten_password')
        activation_token = authorization_services.create_activation_token(activation_data)
        authorization_services.store_activation_token(activation_token)
        password_reset_activation_email(user, activation_token)

    return JSONResponse(status_code=200,
                        content='If there is a user with such an email, an email will be sent.')


@profile_router.get('/password/reset/')
def password_reset(activation_token: str = Query()):
    if not authorization_services.activation_token_exists(activation_token):
        return JSONResponse(status_code=401,
                            content='You are not using a valid token')
    decoded_token = authorization_services.is_authenticated(activation_token)

    try:
        if decoded_token:
            if decoded_token['exp'] > time():
                if decoded_token['purpose'] == 'forgotten_password':
                    generated_password = authorization_services.generate_password()
                    authorization_services.password_changer(decoded_token, generated_password)
                    authorization_services.delete_activation_token(activation_token)
                    password_reset_email(decoded_token, generated_password)
                else:
                    return JSONResponse(status_code=401,
                                        content='You are not using a valid token.')
            else:
                authorization_services.delete_activation_token(activation_token)
                raise ExpiredSignatureError
    except ExpiredSignatureError:
        raise HTTPException(status_code=401,
                            detail='Password reset timelimit has been exceeded. Please request a new password reset.')

    return JSONResponse(status_code=200,
                        content='Your password has been updated. A new password has been sent to your email.')
    # return JSONResponse(status_code=200,
    #                     content=response.json())

