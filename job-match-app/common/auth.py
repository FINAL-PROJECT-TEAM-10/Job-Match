from time import time

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError

from app_models.admin_models import Admin
from services.authorization_services import is_authenticated


# TODO Transform comments for job seekers and companies

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth_2_scheme)):
    credential_exception = HTTPException(status_code=401,
                                         detail='Could not validate credentials',
                                         headers={'WWW-AUTHENTICATE': 'Bearer'})

    try:
        payload = is_authenticated(token)
        username = payload.get("username")
        if username is None:
            raise credential_exception

        if payload['exp'] > time():
            if payload['group'] == 'admins':
                return payload
            # elif payload['group'] == 'job seekers':
            #     if payload['blocked']:
            #         raise HTTPException(status_code=403,
            #                             detail='User has been blocked.')
            #     return JobSeeker.from_query_results(**payload)
            # elif payload['group'] == 'companies':
            #     return Company.from_query_results(**payload)
        else:
            raise ExpiredSignatureError
    except ExpiredSignatureError:
        raise HTTPException(status_code=401,
                            detail='Expired token.')
