from fastapi import APIRouter, Depends

from starlette.responses import JSONResponse, Response

from app_models.admin_models import Admin
from common.auth import get_current_user
from services import admin_services

admin_router = APIRouter(prefix='/admin')


@admin_router.get('/info')
def get_self(current_user: Admin = Depends(get_current_user)):
    return current_user


# TODO: Fix registration

@admin_router.post('/register')
def add_admin(new_admin=Depends(get_current_user)):
    if admin_services.admin_exists(new_admin):
        return JSONResponse(status_code=409,
                            content={'error': 'Admin already exists.'})
    else:
        admin = admin_services.create_admin(new_admin)

    return JSONResponse(status_code=201,
                        content={admin})
