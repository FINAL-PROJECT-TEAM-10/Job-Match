from datetime import datetime

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

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

        if payload['exp'] > datetime.now():
            if payload['group'] == 'admins':
                return Admin.from_query_results(**payload)
            # elif payload['group'] == 'job seekers':
            #     if payload['blocked']:
            #         raise HTTPException(status_code=403,
            #                             detail='User has been blocked.')
            #     return JobSeeker.from_query_results(**payload)
            # elif payload['group'] == 'companies':
            #     return Company.from_query_results(**payload)

    except JWTError:
        raise HTTPException(status_code=401,
                            detail='Expired token.')


class ExpiredException(BaseException):
    '''
    Exception that determines if a token has expired.
    Logic necessary to bypass general exceptions.
    '''

    def __init__(self):
        super().__init__()
        self.message = ('Exception that determines if a token has expired.')
