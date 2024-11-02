from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, List
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
    first_name: str
    last_name: str
    email: str
    gender: int
    password_hash: str
    wallet: str = Field(default="", nullable=True)
    is_admin: bool = False

# utility functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Endpoints
@app.post("/api/user/", status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/user/{user_id}", status_code=status.HTTP_200_OK, response_model=UserBase)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/users/", status_code=status.HTTP_200_OK, response_model=List[UserBase])
async def get_users(db: db_dependency):
    users = db.query(models.User).all()
    return users

@app.post("/api/album/", status_code=status.HTTP_201_CREATED, response_model=AlbumBase)
async def create_album(album: AlbumBase, db: db_dependency):
    db_album = models.Album(**album.dict())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

@app.get("/api/album/{album_id}", status_code=status.HTTP_200_OK, response_model=AlbumBase)
async def get_album(album_id: int, db: db_dependency):
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@app.get("/api/albums/", status_code=status.HTTP_200_OK, response_model=List[AlbumBase])
async def get_albums(db: db_dependency):
    albums = db.query(models.Album).all()
    return albums

@app.post("/api/album/{album_id}/song", status_code=status.HTTP_201_CREATED, response_model=SongBase)
async def create_song(album_id: int, song: SongBase, db: db_dependency):
    db_song = models.Song(**song.dict(), album_fk=album_id)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

@app.get("/api/song={song_id}", status_code=status.HTTP_200_OK)
async def get_song(song_id: int, db: db_dependency):
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@app.get("/api/songs/", status_code=status.HTTP_200_OK, response_model=List[SongBase])
async def get_song(db: db_dependency):
    songs = db.query(models.Song).all()
    return songs