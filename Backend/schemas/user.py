from pydantic import BaseModel
from typing import Optional
from ..models.user import Gender

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    gender: Gender
    password_hash: str
    is_admin: bool = False

class CreateUserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    gender: Gender
    password_hash: str

class UpdateUserBase(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    gender: Gender | None = None
    password_hash: str | None = None
    is_admin: bool = Optional[False]

class Config:
    orm_mode = True
    use_enum_values = True