from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app_models.admin_models import Admin
from app_models.company_models import Company
from app_models.job_seeker_models import JobSeeker
from data.database import read_query, update_query, insert_query
from services import admin_services, job_seeker_services, company_services
from fastapi import HTTPException

# TODO: shorten token expiration
_SECRET_KEY = '2d776838352e75a9f95de915c269c8ce45b12de47f720213c5f71c4e25618c25'
_CUSTOM_SECRET_KEY = 'b1b2c3d4e5f6g7890123456789abcdef0123456789194def0123456789e2186a'
_ALGORITHM = 'HS256'
_TOKEN_EXPIRATION_TIME_MINUTES = timedelta(minutes=1440)
_ACTIVATION_TOKEN_EXPIRATION_TIME_MINUTES = timedelta(minutes=60)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verify_password(text_password, hashed_password):
    return pwd_context.verify(text_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def _get_pass_by_username_admin(username):
    hashed_password = read_query('''
    SELECT password FROM admins WHERE username = ?
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


def authenticate_seeker(username: str, password: str) -> bool | JobSeeker:
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

    if to_encode['group'] != 'admins':
        to_encode.update({'blocked': user_data.blocked})

    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, _SECRET_KEY, algorithm=_ALGORITHM)
    return encoded_jwt


def create_activation_token(activation_data, expiration_delta: timedelta = _ACTIVATION_TOKEN_EXPIRATION_TIME_MINUTES):
    to_encode = {
        "id": activation_data.id,
        "email": activation_data.email,
        "username": activation_data.username,
        "group": activation_data.group,
        "purpose": activation_data.purpose,
    }
    expire = datetime.now() + expiration_delta

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, _CUSTOM_SECRET_KEY, algorithm=_ALGORITHM)

    return encoded_jwt


def is_authenticated(token: str):
    try:
        return jwt.decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=307, detail='Login to proceed')
    
def is_authenticated_custom(token: str):
    return jwt.decode(token, _CUSTOM_SECRET_KEY, algorithms=[_ALGORITHM])


def password_changer(payload, new_password):
    # I tried to use a dynamic table name but the connector threw an error.
    new_password = get_password_hash(new_password)
    if payload['group'] == 'admins':
        return update_query('''UPDATE admins SET password = ? WHERE id = ?''',
                            (new_password, payload['id']))
    if payload['group'] == 'companies':
        return update_query('''UPDATE companies SET password = ? WHERE id = ?''',
                            (new_password, payload['id']))
    if payload['group'] == 'seekers':
        return update_query('''UPDATE job_seekers SET password = ? WHERE id = ?''',
                            (new_password, payload['id']))


def is_password_identical_by_type(payload, password):
    if payload['group'] == 'admins':
        return verify_password(password, _get_pass_by_username_admin(payload['username']))
    elif payload['group'] == 'companies':
        return verify_password(password, _get_pass_by_username_company(payload['username']))
    elif payload['group'] == 'seekers':
        return verify_password(password, _get_pass_by_username_seeker(payload['username']))


def generate_password():
    import random
    import string

    max_length = 15

    lower_case = string.ascii_lowercase
    upper_case = string.ascii_uppercase
    numbers = string.digits
    special_chars = "@$!%*?&"

    password_set = (
            random.choice(lower_case) +
            random.choice(upper_case) +
            random.choice(numbers) +
            random.choice(special_chars))

    password_set += ''.join(
        random.choice(string.ascii_letters + string.digits + special_chars)
        for _ in range(max_length - len(password_set)))

    password_list = list(password_set)
    random.shuffle(password_list)
    return ''.join(password_list)


def activation_token_exists(activation_token):
    return any(read_query('''SELECT id from temporary_tokens WHERE token = ?''',
                          (activation_token,)))


def store_activation_token(activation_token):
    insert_query('''INSERT INTO temporary_tokens (token) VALUES (?)''',
                 (activation_token,))


def delete_activation_token(activation_token):
    update_query('''DELETE FROM temporary_tokens WHERE token = ?''',
                 (activation_token,))

# TODO: Enter your real email after setting up with mailjet to use mailing functionality (installation guide)
# First admin needs to be added because only admins can add other admins
# _first_admin = Admin(username='first_admin',
#                      first_name='Admin',
#                      last_name='Adminov',
#                      email='admin@admin.admin',
#                      phone='1234567890',
#                      post_code='1000',
#                      city='Sofia',
#                      country='Bulgaria')
# _first_admin_pass = 'asdQWE123!@#'
#
# create_admin(_first_admin, _first_admin_pass)
