# TODO Unsure of composition, might refactor later
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app_models.token_models import Token
from services.authorization_services import authenticate_admin, create_access_token

token_router = APIRouter(prefix='/token')

@token_router.post('/', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    admin = authenticate_admin(form_data.username, form_data.password)
    if not admin:
        raise HTTPException(status_code=401,
                            detail='Incorrect username or password.',
                            headers={'WWW-AUTHENTICATE': 'Bearer'})

    access_token = create_access_token(admin)

    return {"access_token": access_token, "token_type": "bearer"}