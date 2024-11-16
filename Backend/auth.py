from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel
from typing import Annotated
from database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from models import User
from database import *

SECRET_KEY = 'htwrjtrjwrtj'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # nwm czy działa
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='api/auth/token')

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return False
    if not bcrypt_context.verify(password, user.password_hash):
        return False
    return user

def create_access_token(username: str, user_id: int, is_admin: bool, expires_delta: timedelta):
    expires = datetime.now(timezone.utc) + expires_delta
    encode = {'sub': username, 'id': user_id, 'is_admin': is_admin, 'exp' : expires}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        is_admin: bool = payload.get('is_admin')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'username': username, 'id': user_id, 'is_admin': is_admin}
    except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

class Token(BaseModel):
    access_token: str
    token_type: str