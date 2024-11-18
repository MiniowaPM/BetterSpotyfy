from sqlalchemy import Column, Integer, String
from ..db import Base

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    genre = Column(String(50), unique=True)