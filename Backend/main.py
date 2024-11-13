from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, List, Optional
from enum import Enum
import models
from models import Gender
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Base Models / Schemas
class AlbumBase(BaseModel):
    title: str
    description: str
    genre: int

class UpdateAlbumBase(BaseModel):
    title: str | None = None
    description: str | None = None
    genre: int | None = None

class SongBase(BaseModel):
    title: str
    description: str
    genre: int

class UpdateSongBase(BaseModel):
    title: str | None = None
    description: str | None = None
    genre: int | None = None

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    gender: Gender
    password_hash: str
    is_admin: bool = False

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

# utility functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# User endpoints
@app.delete("/api/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user in None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)
    return {"detail": "User successfully deleted"}

@app.patch("/api/user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UpdateUserBase, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    return {"detail": "User successfully modified"}

@app.post("/api/user/", status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    check_username = db.query(models.User).filter(models.User.username == db_user.username).first()
    check_email = db.query(models.User).filter(models.User.email == db_user.email).first()
    if check_username is not None:
        raise HTTPException(status_code=409, detail="Username already exists")
    if check_email is not None:
        raise HTTPException(status_code=409, detail="Email already exists")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"detail": "User successfully created"}


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

# Album endpoints
@app.delete("/api/album/{album_id}", status_code=status.HTTP_200_OK)
async def delete_album(album_id: int, db: db_dependency):
    db_album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if db_album in None:
        raise HTTPException(status_code=404, detail="Album not found")
    db.query(models.Song).filter(models.Song.album_fk == album_id).update({models.Song.album_fk: None})
    db.delete(db_album)
    db.commit()
    db.refresh(db_album)
    return {"detail": "Album and associated foreign keys successfully cleared"}

@app.patch("/api/album/{album_id}", status_code=status.HTTP_200_OK)
async def update_user(album_id: int, album: UpdateAlbumBase, db: db_dependency):
    db_album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if db_album is None: 
        raise HTTPException(status_code=404, detail="Album not found")
    for key, value in album.model_dump(exclude_unset=True).items():
        setattr(db_album, key, value)
    db.commit()
    return {"detail": "Album successfully modified"}

@app.post("/api/album/", status_code=status.HTTP_201_CREATED, response_model=AlbumBase)
async def create_album(album: AlbumBase, db: db_dependency):
    db_album = models.Album(**album.model_dump())
    check_genre = db.query(models.Album).filter(models.Album.genre == db_album.genre).first()
    check_title = db.query(models.Album).filter(models.Album.title == db_album.title).first()
    if check_title is not None:
        raise HTTPException(status_code=409, detail="Title already exists")
    if check_genre is None:
        raise HTTPException(status_code=409, detail="Invalid genre type")
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return {"detail": "Album successfully created"}

@app.get("/api/album/{album_id}", status_code=status.HTTP_200_OK, response_model=AlbumBase)
async def get_album(album_id: int, db: db_dependency):
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@app.get("/api/albums/", status_code=status.HTTP_200_OK, response_model=List[AlbumBase])
async def get_albums(db: db_dependency):
    albums = db.query(models.Album).all()
    if albums is None:
        raise HTTPException(status_code=404, detail="Albums not found")
    return albums

# Song endpoints
@app.delete("/api/song/{song_id}", status_code=status.HTTP_200_OK)
async def delete_song(song_id: int, db: db_dependency):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song in None:
        raise HTTPException(status_code=404, detail="Song not found")
    db.delete(db_song)
    db.commit()
    db.refresh(db_song)
    return {"detail": "Song successfully cleared"}

@app.patch("/api/song/{song_id}", status_code=status.HTTP_200_OK)
async def update_user(song_id: int, song: UpdateSongBase, db: db_dependency):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song is None: 
        raise HTTPException(status_code=404, detail="Song not found")
    for key, value in song.model_dump(exclude_unset=True).items():
        setattr(db_song, key, value)
    db.commit()
    return {"detail": "Song successfully modified"}

@app.post("/api/album/{album_id}/song", status_code=status.HTTP_201_CREATED, response_model=SongBase)
async def create_song(album_id: int, song: SongBase, db: db_dependency):
    db_song = models.Song(**song.model_dump(), album_fk=album_id)
    check_album_id = db.query(models.Song).filter(models.Song.id == db_song.id).first()
    check_title = db.query(models.Song).filter(models.Song.title == db_song.title).first()
    if check_album_id is None:
        raise HTTPException(status_code=404, detail="Album id not found")
    if check_title is not None:
        raise HTTPException(status_code=409, detail="Title already exists")
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return {"detail": "Song and associated foreign key successfully created"}

@app.get("/api/song/{song_id}", status_code=status.HTTP_200_OK)
async def get_song(song_id: int, db: db_dependency):
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@app.get("/api/songs/", status_code=status.HTTP_200_OK, response_model=List[SongBase])
async def get_song(db: db_dependency):
    songs = db.query(models.Song).all()
    if songs is None:
        raise HTTPException(status_code=404, detail="Songs not found")
    return songs