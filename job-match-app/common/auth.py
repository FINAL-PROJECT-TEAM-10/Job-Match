from datetime import datetime

from fastapi import HTTPException

from app_models.admin_models import Admin
from services.authorization_service import is_authenticated


# TODO Transform comments for job seekers and companies
# TODO move from service to here
# def logged_in_or_401(token: str):
#     try:
#         payload = is_authenticated(token)
#
#         if payload['exp'] > datetime.now():
#             if payload['group'] == 'admins':
#                 return Admin.from_query_results(**payload)
#             # elif payload['group'] == 'job seekers':
#             #     return JobSeeker.from_query_results(**payload)
#             # elif payload['group'] == 'companies':
#             #     return Company.from_query_results(**payload)
#         else:
#             raise ExpiredException
#     except ExpiredException:
#         raise HTTPException(status_code=401,
#                             detail='Expired token.')
        # raise HTTPException(status_code=401)


class ExpiredException(BaseException):
    '''
    Exception that determines if a token has expired.
    Logic necessary to bypass general exceptions.
    '''

    def __init__(self):
        super().__init__()
        self.message = ('Exception that determines if a token has expired.')
