from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ... import models, schemas, db
from ...api.dependencies.auth import user_dependency
from ... api.dependencies.db import db_dependency
from ...schemas.user import UpdateUserBase, CreateUserBase
from ...schemas.response import SuccessResponse
from ...core.security import bcrypt_context

router = APIRouter(prefix="/user")

@router.delete("/{user_id}", tags=["User"], status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency, user_auth: user_dependency):
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User successfully deleted"}

@router.patch("/{user_id}", tags=["User"], status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user: UpdateUserBase, db: db_dependency, user_auth: user_dependency):
    if user_id == "current":
        user_id = user_auth["id"]
    else:
        user_id = int(user_id)
    if user_id is not user_auth["id"] and not user_auth.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        if key == "password_hash":
            value = bcrypt_context.hash(user.password_hash)
        if key == "is_admin" and user_auth.get("is_admin", False) is False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must be an admin to change the is_admin field")
        setattr(db_user, key, value)
    db.commit()
    return {"detail": "User successfully modified"}

@router.post("/", tags=["User"], status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
async def create_user(user: CreateUserBase, db: db_dependency):
    password_bcrypt_hash = bcrypt_context.hash(user.password_hash)
    db_user =  models.User(**{**user.model_dump(), "password_hash": password_bcrypt_hash})
    check_username = db.query(models.User).filter(models.User.username == db_user.username).first()
    check_email = db.query(models.User).filter(models.User.email == db_user.email).first()
    if check_username is not None:
        raise HTTPException(status_code=409, detail="Username already exists")
    if check_email is not None:
        raise HTTPException(status_code=409, detail="Email already exists")
    db.add(db_user)
    db.commit()
    return {"detail": "User successfully created"}

@router.get("/{user_id}", tags=["User"], status_code=status.HTTP_200_OK, response_model=UpdateUserBase)
async def get_user(user_id: str, db: db_dependency, user_auth: user_dependency):
    if user_id == "current":
        user_id = user_auth["id"]
    else:
        user_id = int(user_id)
    if user_auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_auth.get("is_admin", False) and user_id != user_auth["id"]:
        user.password_hash = None
        user.is_admin = False
        user.wallet = None
    return user

@router.get("/all", tags=["User"], status_code=status.HTTP_200_OK, response_model=List[UpdateUserBase])
async def get_users(db: db_dependency, user_auth: user_dependency):
    users = db.query(models.User).all()
    if not user_auth.get("is_admin", False):
        for user in users:
            user.password_hash = None
            user.is_admin = False
            user.wallet = None
    return users