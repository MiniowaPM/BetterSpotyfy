from sqlalchemy import Column, Integer, String, ForeignKey
from ..db import Base

class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True)
    description = Column(String(500), unique=False)
    genre = Column(Integer, ForeignKey('genres.id'))
    album_fk = Column(Integer, ForeignKey('albums.id'))