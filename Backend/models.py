from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Gender(Base):
    __tablename__ = 'gender'

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(50), unique=True)

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    genre = Column(String(50), unique=True)

class Songs_owned(Base):
    __tablename__ = 'songs_owned'
    
    id = Column(Integer, primary_key=True, index=True)
    song_fk = Column(Integer, ForeignKey('songs.id'))
    user_fk = Column(Integer, ForeignKey('users.id'))
    create_date = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(50), unique=False)
    last_name = Column(String(50), unique=False)
    email = Column(String(100), unique=True)
    gender = Column(Integer, ForeignKey('gender.id'))
    password_hash = Column(String(128), unique=False)
    wallet = Column(String(50), unique=False, nullable=True)
    is_admin = Column(Boolean, unique=False, default=False)

class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True)
    description = Column(String(500), unique=False)
    genre = Column(Integer, ForeignKey('genres.id'))

class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True)
    description = Column(String(500), unique=False)
    genre = Column(Integer, ForeignKey('genres.id'))
    album_fk = Column(Integer, ForeignKey('albums.id'))