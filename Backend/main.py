from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated, List, Optional
from enum import Enum
import models
from models import Gender
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from auth import *
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime


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

class SuccessResponse(BaseModel):
    detail: str

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
user_dependency = Annotated[dict, Depends(get_current_user)]

# User endpoints
@app.delete("/api/user/{user_id}", tags=["User"], status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency, user_auth: user_dependency):
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User successfully deleted"}

@app.patch("/api/user/{user_id}", tags=["User"], status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user: UpdateUserBase, db: db_dependency, user_auth: user_dependency):
    if user_id == "current":
        user_id = user_auth["id"]
    else:
        user_id = int(user_id)
    if user_id is not user_auth["id"] and not user_auth.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        if key == "password_hash":
            value = bcrypt_context.hash(user.password_hash)
        if key == "is_admin" and user_auth.get("is_admin", False) is False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must be an admin to change the is_admin field")
        setattr(db_user, key, value)
    db.commit()
    return {"detail": "User successfully modified"}

@app.post("/api/user/", tags=["User"], status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
async def create_user(user: CreateUserBase, db: db_dependency):
    password_bcrypt_hash = bcrypt_context.hash(user.password_hash)
    db_user =  models.User(**{**user.model_dump(), "password_hash": password_bcrypt_hash})
    check_username = db.query(models.User).filter(models.User.username == db_user.username).first()
    check_email = db.query(models.User).filter(models.User.email == db_user.email).first()
    if check_username is not None:
        raise HTTPException(status_code=409, detail="Username already exists")
    if check_email is not None:
        raise HTTPException(status_code=409, detail="Email already exists")
    db.add(db_user)
    db.commit()
    return {"detail": "User successfully created"}

@app.get("/api/user/{user_id}", tags=["User"], status_code=status.HTTP_200_OK, response_model=UpdateUserBase)
async def get_user(user_id: str, db: db_dependency, user_auth: user_dependency):
    if user_id == "current":
        user_id = user_auth["id"]
    else:
        user_id = int(user_id)
    if user_auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_auth.get("is_admin", False) and user_id != user_auth["id"]:
        user.password_hash = None
        user.is_admin = False # If user is non admin, is_admin is hidden (always false)
        user.wallet = None
    return user

@app.get("/api/users/", tags=["User"], status_code=status.HTTP_200_OK, response_model=List[UpdateUserBase])
async def get_users(db: db_dependency, user_auth: user_dependency):
    users = db.query(models.User).all()
    if not user_auth.get("is_admin", False):
        for user in users:
            user.password_hash = None
            user.is_admin = False
            user.wallet = None
    return users

# Album endpoints
@app.delete("/api/album/{album_id}", tags=["Album"], status_code=status.HTTP_200_OK)
async def delete_album(album_id: int, db: db_dependency, user_auth: user_dependency):
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    db.query(models.Song).filter(models.Song.album_fk == album_id).update({models.Song.album_fk: None})
    db.delete(db_album)
    db.commit()
    return {"detail": "Album and associated foreign keys successfully cleared"}

@app.patch("/api/album/{album_id}", tags=["Album"], status_code=status.HTTP_200_OK)
async def update_user(album_id: int, album: UpdateAlbumBase, db: db_dependency, user_auth: user_dependency):
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    if user_auth is None or not user_auth.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if db_album is None: 
        raise HTTPException(status_code=404, detail="Album not found")
    for key, value in album.model_dump(exclude_unset=True).items():
        setattr(db_album, key, value)
    db.commit()
    return {"detail": "Album successfully modified"}

@app.post("/api/album/", tags=["Album"], status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
async def create_album(album: AlbumBase, db: db_dependency, user_auth: user_dependency):
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_album = models.Album(**album.model_dump())
    check_genre = db.query(models.Genre).filter(models.Genre.id == db_album.genre).first()
    check_title = db.query(models.Album).filter(models.Album.title == db_album.title).first()
    if check_title is not None:
        raise HTTPException(status_code=409, detail="Title already exists")
    if check_genre is None:
        raise HTTPException(status_code=409, detail="Invalid genre type")
    db.add(db_album)
    db.commit()
    return {"detail": "Album successfully created"}

@app.get("/api/album/{album_id}", tags=["Album"], status_code=status.HTTP_200_OK, response_model=AlbumBase)
async def get_album(album_id: int, db: db_dependency, user_auth: user_dependency):
    if user_auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@app.get("/api/albums/", tags=["Album"], status_code=status.HTTP_200_OK, response_model=List[AlbumBase])
async def get_albums(db: db_dependency, user_auth: user_dependency):
    if user_auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    albums = db.query(models.Album).all()
    if albums is None:
        raise HTTPException(status_code=404, detail="Albums not found")
    return albums

# Song endpoints
@app.delete("/api/song/{song_id}", tags=["Song"], status_code=status.HTTP_200_OK)
async def delete_song(song_id: int, db: db_dependency, user_auth: user_dependency):
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    db.delete(db_song)
    db.commit()
    return {"detail": "Song successfully cleared"}

@app.patch("/api/song/{song_id}", tags=["Song"], status_code=status.HTTP_200_OK)
async def update_user(song_id: int, song: UpdateSongBase, db: db_dependency, user_auth: user_dependency):
    if user_auth is None or not user_auth.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song is None: 
        raise HTTPException(status_code=404, detail="Song not found")
    for key, value in song.model_dump(exclude_unset=True).items():
        setattr(db_song, key, value)
    db.commit()
    return {"detail": "Song successfully modified"}

@app.post("/api/album/{album_id}/song", tags=["Song"], status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
async def create_song(album_id: int, song: SongBase, db: db_dependency, user_auth: user_dependency):
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_song = models.Song(**song.model_dump(), album_fk=album_id)
    check_album_id = db.query(models.Album).filter(models.Album.id == album_id).first()
    check_title = db.query(models.Song).filter(models.Song.title == db_song.title).first()
    if check_album_id is None:
        raise HTTPException(status_code=404, detail="Album id not found")
    if check_title is not None:
        raise HTTPException(status_code=409, detail="Title already exists")
    db.add(db_song)
    db.commit()
    return {"detail": "Song and associated foreign key successfully created"}

@app.get("/api/song/{song_id}", tags=["Song"], status_code=status.HTTP_200_OK)
async def get_song(song_id: int, db: db_dependency, user_auth: user_dependency):
    if user_auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@app.get("/api/songs/", tags=["Song"], status_code=status.HTTP_200_OK, response_model=List[SongBase])
async def get_song(db: db_dependency, user_auth: user_dependency):
    if user_auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    songs = db.query(models.Song).all()
    if songs is None:
        raise HTTPException(status_code=404, detail="Songs not found")
    return songs

# Authentication endpoints
@app.post("/api/auth/token", tags=["Auth"], status_code=status.HTTP_201_CREATED, response_model=Token)
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to validate user")
    token = create_access_token(user.username, user.id, user.is_admin, timedelta(minutes=30))
    return {'access_token': token, 'token_type':'bearer'}