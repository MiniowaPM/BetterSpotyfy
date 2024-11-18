from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from ... import models, schemas, db
from .. import db_dependency
from ...schemas import Token
from ..dependencies import authenticate_user, create_access_token
from datetime import timedelta


router = APIRouter(prefix="/auth")

@router.post("/token", tags=["Auth"], status_code=status.HTTP_201_CREATED, response_model=Token)
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to validate user")
    token = create_access_token(user.username, user.id, user.is_admin, timedelta(minutes=30))
    return {'access_token': token, 'token_type':'bearer'}