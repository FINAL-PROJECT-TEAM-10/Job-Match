from fastapi import APIRouter, Depends

from starlette.responses import JSONResponse

from app_models.admin_models import Admin
from services.authorization_service import get_current_user

admin_router = APIRouter(prefix='/admin')

@admin_router.get('/info')
def get_self(current_user: Admin = Depends(get_current_user)):
    return current_user