from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ... import models, schemas, db
from ...schemas import AlbumBase, UpdateAlbumBase, SuccessResponse
from .. import db_dependency, user_dependency

router = APIRouter(prefix="/album")

@router.delete("/{album_id}", tags=["Album"], status_code=status.HTTP_200_OK)
async def delete_album(album_id: int, db: db_dependency, user_auth: user_dependency):
    # Check for JWT token stored user_id or user permissions (is_admin == 1)
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    db.query(models.Song).filter(models.Song.album_fk == album_id).update({models.Song.album_fk: None})
    db.delete(db_album)
    db.commit()
    return {"detail": "Album and associated foreign keys successfully cleared"}

@router.patch("/{album_id}", tags=["Album"], status_code=status.HTTP_200_OK)
async def update_user(album_id: int, album: UpdateAlbumBase, db: db_dependency, user_auth: user_dependency):
    # Check for JWT token stored user_id or user permissions (is_admin == 1)
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if db_album is None: 
        raise HTTPException(status_code=404, detail="Album not found")
    # For each patched (inserted) element set an attribute of selected record
    for key, value in album.model_dump(exclude_unset=True).items():
        setattr(db_album, key, value)
    db.commit()
    return {"detail": "Album successfully modified"}

@router.post("/", tags=["Album"], status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
async def create_album(album: AlbumBase, db: db_dependency, user_auth: user_dependency):
    # Check for JWT token stored user_id or user permissions (is_admin == 1)
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

@router.get("/{album_id}", tags=["Album"], status_code=status.HTTP_200_OK, response_model=AlbumBase)
async def get_album(album_id: int, db: db_dependency, user_auth: user_dependency):
    # Check for JWT token whether is valid
    if user_auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@router.get("/all", tags=["Album"], status_code=status.HTTP_200_OK, response_model=List[AlbumBase])
async def get_albums(db: db_dependency, user_auth: user_dependency):
    # Check for JWT token whether is valid
    if user_auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    albums = db.query(models.Album).all()
    if albums is None:
        raise HTTPException(status_code=404, detail="Albums not found")
    return albums