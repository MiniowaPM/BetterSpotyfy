from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..db import Base

class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True)
    description = Column(String(500), unique=False)
    genre = Column(Integer, ForeignKey('genres.id'))