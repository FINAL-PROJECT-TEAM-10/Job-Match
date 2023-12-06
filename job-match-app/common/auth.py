from time import time
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError
from pydantic import BaseModel

from services.authorization_services import is_authenticated

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#  Currently the token verifies against the database.
#  If we want to go for statelessness the access token should not verify each time
#  against the database. Instead, there should be a whitelist/blacklist that could
#  be in memory. Additional functionality could be adding refresh tokens.

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
            elif payload['group'] == 'seekers':
                if payload['blocked']:
                    raise HTTPException(status_code=403,
                                        detail='User has been blocked.')
                return payload
            elif payload['group'] == 'companies':
                return payload
        else:
            raise ExpiredSignatureError
    except ExpiredSignatureError:
        raise HTTPException(status_code=401,
                            detail='Expired token.')

class TokenInfo(BaseModel):
    id: int
    group: str
    username: str
    email: str
