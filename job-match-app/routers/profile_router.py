import io
from time import time
from fastapi import HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends, Body, Query, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from jose import ExpiredSignatureError

from app_models.input_models import PasswordUpdater
from app_models.token_models import ActivationDataModel
from common.auth import TokenInfo, get_current_user
from common.mailing import password_reset_email, password_reset_activation_email
from services import authorization_services, company_services, job_seeker_services, admin_services, upload_services
from services.upload_services import is_file_jpeg

profile_router = APIRouter(prefix='/profile', tags={'Profile info and password management'})


@profile_router.get('/info', response_model=TokenInfo,
                    responses={200: {"description": "Informs the user of basic info, which is included in the token."}})
def get_self(current_user_payload=Depends(get_current_user)):
    
    return current_user_payload


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
def forgotten_password_activation_link(email: str = Query(), user_type: str = Query()):
    fake_payload = {}
    if user_type == 'admins':
        user = admin_services.get_admin_by_email(email)
    elif user_type == 'companies':
        user = company_services.get_company_by_email(email)
    elif user_type == 'job_seekers':
        user = job_seeker_services.get_seeker_by_email(email)
    else:
        raise HTTPException(status_code=400,
                            detail='Invalid user type category.'
                                    'Categories can be: admins, companies, job_seekers')

    if user:
        activation_data = ActivationDataModel(id=user.id,
                                              email=user.email,
                                              username=user.username,
                                              group=user.group,
                                              purpose='forgotten_password')
        activation_token = authorization_services.create_activation_token(activation_data)
        authorization_services.store_activation_token(activation_token)
        password_reset_activation_email(user, activation_token)

    raise HTTPException(status_code=200,
                        detail='If there is a user with such an email, an email will be sent.')


@profile_router.get('/password/reset/')
def password_reset(activation_token: str = Query()):
    if not authorization_services.activation_token_exists(activation_token):
        return JSONResponse(status_code=401,
                            content='You are not using a valid token')
    decoded_token = authorization_services.is_authenticated_custom(activation_token)

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


@profile_router.get('/picture')
def get_avatar(current_user_payload=Depends(get_current_user)):
    image_data = upload_services.get_picture(current_user_payload['id'], current_user_payload['group'])

    if image_data is None:
        return JSONResponse(status_code=404,
                            content='You have not uploaded a picture to your profile.')

    return StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")


@profile_router.post('/picture')
def upload_picture(image_file: UploadFile, current_user_payload=Depends(get_current_user)):
    try:
        # NOTE: After spending hours on investigating why the image was not returned,
        # I found out that checking jpeg format leads to a hidden truncation of the image
        # data. Possibly because the method from PIL has to read a part of the file and
        # does not restore the cursor.
        # If the seek cursor is restored, the image is no longer truncated.
        # If the seek cursor is not restored after the check,
        # the image becomes corrupt.

        if not is_file_jpeg(image_file):
            return JSONResponse(status_code=400,
                                content='Server accepts only jpg/jpeg as picture formats.')
        image_file.file.seek(0)
        max_file_size_bytes = 1024 * 1024
        # Interestingly, .size does not affect the reading of the image.
        if image_file.size > max_file_size_bytes:
            return JSONResponse(status_code=413,
                                content=f'Image file too big. Please upload a file that is less than 1 MB.')

        # image_file.file.seek(0)
        image_data = image_file.file.read()
        upload_services.upload_picture(current_user_payload, image_data)

        return JSONResponse(status_code=201,
                            content=f"Image {image_file.filename} uploaded successfully")
    except Exception as e:
        return JSONResponse(status_code=422,
                            content=f"An error occurred: {e}")
