from fastapi import FastAPI, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

_SECRET_KEY = '2d776838352e75a9f95de915c269c8ce45b12de47f720213c5f71c4e25618c25'
_ALGORITHM = 'HS256'
_TOKEN_EXPIRATION_TIME_MINUTES = 1440