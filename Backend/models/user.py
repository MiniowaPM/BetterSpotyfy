from sqlalchemy import Column, Integer, String, Enum, Boolean
from ..db import Base
import enum

class Gender(enum.Enum):
    Male = 1
    Female = 2
    Other = 3

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(50), unique=False)
    last_name = Column(String(50), unique=False)
    email = Column(String(100), unique=True)
    gender = Column(Enum(Gender), nullable=False)
    password_hash = Column(String(128), unique=False)
    wallet = Column(String(50), unique=False, nullable=True)
    is_admin = Column(Boolean, unique=False, default=False)