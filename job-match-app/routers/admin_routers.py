from typing import Annotated

from fastapi import APIRouter, Depends, Body

from fastapi.responses import JSONResponse, Response

from app_models.admin_models import Admin
from common.auth import get_current_user, TokenInfo
from services import admin_services

admin_router = APIRouter(prefix='/admin')


@admin_router.get('/info', response_model=TokenInfo,
                  responses={200: {"description": "Informs the user of basic info, which is included in the token."}})
def get_self(current_user_payload=Depends(get_current_user)):
    return JSONResponse(status_code=200,
                        content=current_user_payload)


# TODO: Fix registration

@admin_router.post('/register', response_model=Admin, responses={
    201: {"description": "Informs of admin creation",
          "content": {"application/json": {"example": {"id": 1,
                                                       "group": "admins",
                                                       "username": "example_admin",
                                                       "email": "admin@example.com"
                                                       }
                                           }
                      }
          },
    403: {"description": "Checks privileges.",
          "content": {
            "text/plain": {
                "example": "Only admins can register other admins."
            }
        }
    },
    409: {
        "description": "Assures admin uniqueness.",
        "content": {
            "text/plain": {"example": "Admin [USERNAME] already exists."}
                   }
        }
})
def add_admin(registration_details: Admin, password: Annotated[str, Body()], current_user_payload=Depends(get_current_user)):
    if current_user_payload['group'] != 'admins':
        return JSONResponse(status_code=403,
                            content='Only admins can register other admins.')

    if admin_services.admin_exists(registration_details):
        return JSONResponse(status_code=409,
                            content=f'Admin with username {registration_details.username} already exists.')

    new_admin = admin_services.create_admin(registration_details, password)
    return JSONResponse(status_code=201,
                        content=new_admin.json())
