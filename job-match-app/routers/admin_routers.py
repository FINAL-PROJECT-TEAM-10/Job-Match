from typing import Annotated

from fastapi import APIRouter, Depends, Body

from fastapi.responses import JSONResponse, Response

from app_models.admin_models import Admin
from common.auth import get_current_user, TokenInfo
from common.country_validators_helpers import validate_location
from services import admin_services

admin_router = APIRouter(prefix='/admin',tags={'Only for Admins'})


# TODO: Fix registration
#  Test registration to see if to do is still relevant.

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

    validate_location(registration_details.city, registration_details.country)

    if registration_details.group != 'admins':
        return JSONResponse(status_code=400,
                            content='This is an endpoint for creating admins only.')
    new_admin = admin_services.create_admin(registration_details, password)
    return JSONResponse(status_code=201,
                        content=new_admin.json())


# TODO: Implement mailing history for admins

