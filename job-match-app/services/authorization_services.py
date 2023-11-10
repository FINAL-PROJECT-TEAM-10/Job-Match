from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app_models.admin_models import Admin
from data.database import read_query
from services import admin_services, job_seeker_services, company_services

_SECRET_KEY = '2d776838352e75a9f95de915c269c8ce45b12de47f720213c5f71c4e25618c25'
_ALGORITHM = 'HS256'
_TOKEN_EXPIRATION_TIME_MINUTES = timedelta(minutes=1440)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verify_password(text_password, hashed_password):
    return pwd_context.verify(text_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def _get_pass_by_username_admin(username):
    hashed_password = read_query('''
    SELECT password FROM admin_list WHERE username = ?
    ''', (username,))

    if hashed_password:
        hashed_password = hashed_password[0][0]
        return hashed_password
    else:
        return None


def _get_pass_by_username_seeker(username):
    hashed_password = read_query('''
    SELECT password FROM job_seekers WHERE username = ?
    ''', (username,))

    if hashed_password:
        hashed_password = hashed_password[0][0]
        return hashed_password
    else:
        return None


def _get_pass_by_username_company(username):
    hashed_password = read_query('''
    SELECT password FROM companies WHERE username = ?
    ''', (username,))

    if hashed_password:
        hashed_password = hashed_password[0][0]
        return hashed_password
    else:
        return None


def authenticate_admin(username: str, password: str) -> bool | Admin:
    admin = admin_services.get_admin(username)
    if not admin:
        return False
    if not verify_password(password, _get_pass_by_username_admin(username)):
        return False

    return admin


def authenticate_seeker(username: str, password: str) -> bool | Job_Seeker:
    seeker = job_seeker_services.get_seeker(username)
    if not seeker:
        return False
    if not verify_password(password, _get_pass_by_username_seeker(username)):
        return False

    return seeker


def authenticate_company(username: str, password: str) -> bool | Company:
    company = company_services.get_company(username)
    if not company:
        return False
    if not verify_password(password, _get_pass_by_username_company(username)):
        return False

    return company


def create_access_token(user_data, expiration_delta: timedelta = _TOKEN_EXPIRATION_TIME_MINUTES):
    to_encode = {
        "id": user_data.id,
        "group": user_data.group,
        "username": user_data.username,
        "email": user_data.email
    }
    expire = datetime.now() + expiration_delta
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, _SECRET_KEY, algorithm=_ALGORITHM)
    return encoded_jwt


def is_authenticated(token: str):
    return jwt.decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
