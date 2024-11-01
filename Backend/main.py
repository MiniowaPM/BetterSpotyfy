from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Base Models / Schemas
class AlbumBase(BaseModel):
    title: str
    description: str
    genre: int

class SongBase(BaseModel):
    title: str
    description: str
    genre: int

class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str
    gender: str
    password: str


# utility functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Endpoints
@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(user)
    db.commit()

@app.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user: UserBase, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/album", status_code=status.HTTP_201_CREATED)
async def create_album(album: AlbumBase, db: db_dependency):
    db_album = models.Album(**album.dict())
    db.add(album)
    db.commit()

@app.get("/album/{album_id}", status_code=status.HTTP_200_OK)
async def get_album(user: AlbumBase, db: db_dependency):
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=404, detail="User not found")
    return album

@app.post("/album={album_id}/song", status_code=status.HTTP_201_CREATED)
async def create_song(song: SongBase, db: db_dependency):
    db_songs = models.Song(**song.dict())
    db.add(song)
    db.commit()

@app.get("/song={song_id}", status_code=status.HTTP_200_OK)
async def get_song(song: SongBase, db: db_dependency):
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if song and album is None:
        raise HTTPException(status_code=404, detail="User not found")
    return song