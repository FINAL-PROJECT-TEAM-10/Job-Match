from fastapi import FastAPI, Depends, status, HTTPException


from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app_models.admin_models import Admin
from data.database import read_query

_SECRET_KEY = '2d776838352e75a9f95de915c269c8ce45b12de47f720213c5f71c4e25618c25'
_ALGORITHM = 'HS256'
_TOKEN_EXPIRATION_TIME_MINUTES = 1440

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verify_password(text_password, hashed_password):
    return pwd_context.verify(text_password, hashed_password)


# TODO: Hashing is not working properly, may be not interpreted by the database correctly
def get_password_hash(password):
    return pwd_context.hash(password)


def get_pass_by_username_admin(username):
    hashed_password = read_query ('''
    SELECT password FROM admin_list WHERE username = ?
    ''', (username,))

    if hashed_password:
        hashed_password = hashed_password[0][0].decode('utf-8')
        return hashed_password
    else:
        return None

def get_admin(username):
    admin_data = read_query('''
    SELECT a.id, a.username, a.first_name, a.last_name, a.picture, c.email, c.address, c.telephone, c.post_code, l.city, l.country
    FROM admin_list as a, employee_contacts as c, locations as l 
    WHERE a.employee_contacts_id = c.id AND c.locations_id = l.id
    AND a.username = ?
    ''', (username,))

    return next((Admin.from_query_results(*row) for row in admin_data), None)
def authenticate_admin(username: str, password: str) -> bool:
    admin = get_admin(username)
    if not admin:
        return False
    if not verify_password(password, get_pass_by_username_admin(username)):
        return False

    return admin

def create_access_token(data, expiration_delta: timedelta = _TOKEN_EXPIRATION_TIME_MINUTES):
    to_encode = data.copy()
    expire = datetime.now() + expiration_delta
    to_encode['exp'] = expire

    encoded_jwt = jwt.encode(to_encode, _SECRET_KEY, algorithm=_ALGORITHM)
    return encoded_jwt

def is_authenticated(token: str):
    return jwt.decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])



