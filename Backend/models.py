from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship 
from database import Base

class Gender(Base):
    __tablename__ = 'gender'

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(50), unique=True)

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    genre = Column(String(50), unique=True)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    first_name = Column(String(50), unique=False)
    last_name = Column(String(50), unique=False)
    email = Column(String(50), unique=True)
    gender = Column(Integer, ForeignKey("gender.id"))
    password_hash = Column(String(50), unique=True)
    wallet = Column(String(50), unique=False)

class Songs_owned(Base):
    __tablename__ = 'songs_owned'
    
    id = Column(Integer, primary_key=True, index=True)
    # song_fk =
    # user_fk =
    # creadte_date =

class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True)
    description = Column(String(500), unique=False)
    # genre = Column(String(50), unique=False) <- FK to a genre table

class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True)
    description = Column(String(500), unique=False)
    genre = Column(String(50), unique=False)
    # album_fk = Column(Integer)