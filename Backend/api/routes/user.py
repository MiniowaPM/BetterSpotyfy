from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path
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
    # Check for JWT token and user permissions (is_admin == 1)
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    # User does not exists in database
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User successfully deleted"}

@router.patch("/{user_id}", tags=["User"], status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user: UpdateUserBase, db: db_dependency, user_auth: user_dependency):
    # check the {user_id} variable for str == me or int
    if user_id == "me":
        user_id = user_auth["id"]
    else:
        user_id = int(user_id)
    # Check for JWT token stored user_id or user permissions (is_admin == 1)
    if user_id is not user_auth["id"] and not user_auth.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    # User does not exists in database
    if db_user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    # For each patched (inserted) element set an attribute of selected record
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

@router.get("/all", tags=["User"], status_code=status.HTTP_200_OK, response_model=List[UpdateUserBase])
async def get_users(db: db_dependency, user_auth: user_dependency):
    users = db.query(models.User).all()
    # User does not exists in database
    if users is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no users in database")
    # Clear extra info if user does not have admin permisions | TODO: zmiana z usuwania wartości do usunięcia argumentów ze słownika
    if not user_auth.get("is_admin", False):
        for user in users:
            user.password_hash = None
            user.is_admin = False
            user.wallet = None
    return users

@router.get("/{user_id}", tags=["User"], status_code=status.HTTP_200_OK, response_model=UpdateUserBase)
async def get_user(user_id: str, db: db_dependency, user_auth: user_dependency):
    # check the {user_id} variable for str == me or int
    if user_id == "me":
        user_id = user_auth["id"]
    else:
        user_id = int(user_id)
    # Check for JWT token whether user logged
    if user_auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Clear extra info if user does not have admin permisions | TODO: zmiana z usuwania wartości do usunięcia argumentów ze słownika
    if not user_auth.get("is_admin", False) and user_id != user_auth["id"]:
        user.password_hash = None
        user.is_admin = False
        user.wallet = None
    return user

@router.post("/me/profile-image/",  tags=["User"], status_code=status.HTTP_200_OK, response_model=SuccessResponse)
async def upload_user_profile_image(user_auth: user_dependency, file: UploadFile):
    base_dir = Path(__file__).resolve().parent.parent.parent
    # Check for file extention
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Only .jpg, .jpeg, .png are allowed.")
    image_path = base_dir/"images"/"users"/ f"{user_auth["id"]}.jpg"
    if user_auth is None:
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    try:
        with open(image_path, "wb") as f:
            f.write(await file.read())
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File failed to create")
    return {"detail": "User profile image succesfuly created"}

@router.get("/{user_id}/profile-image", tags=["User"], status_code=status.HTTP_200_OK)
async def get_user_profile_image(user_id: str, user_auth: user_dependency):
    if user_id == "me":
        user_id = user_auth["id"]
    else:
        user_id = int(user_id)
    if user_auth is None:
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    base_dir = Path(__file__).resolve().parent.parent.parent
    image_path = base_dir/"images"/"users"/f"{user_id}.jpg"
    if not image_path.is_file():
        image_path = base_dir/"images"/"users"/"default.jpg"
    return FileResponse(image_path)