from fastapi import APIRouter

from starlette.responses import JSONResponse

admin_router = APIRouter(prefix='/admin')

@admin_router.get('/')
def all_admins(x_token=Header()):
    if