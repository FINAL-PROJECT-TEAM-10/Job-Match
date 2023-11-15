from typing import Annotated

from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse

from app_models.input_models import PasswordUpdater
from common.auth import TokenInfo, get_current_user
from services import authorization_services

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
