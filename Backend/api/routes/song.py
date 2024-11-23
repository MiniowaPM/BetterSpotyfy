from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ... import models, schemas, db
from .. import db_dependency, user_dependency
from ...schemas import SongBase, UpdateSongBase, SuccessResponse

router = APIRouter(prefix="/song")

@router.delete("/{song_id}", tags=["Song"], status_code=status.HTTP_200_OK)
async def delete_song(song_id: int, db: db_dependency, user_auth: user_dependency):
    # Logged JWT Token validation and user permisions
    if user_auth is None or not user_auth.get('is_admin', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    db.delete(db_song)
    db.commit()
    return {"detail": "Song successfully cleared"}

@router.patch("/{song_id}", tags=["Song"], status_code=status.HTTP_200_OK)
async def update_user(song_id: int, song: UpdateSongBase, db: db_dependency, user_auth: user_dependency):
    # Logged JWT Token validation and user permisions
    if user_auth is None or not user_auth.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed or insufficient premissions')
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song is None: 
        raise HTTPException(status_code=404, detail="Song not found")
    # For each patched (inserted) element set an attribute of selected record
    for key, value in song.model_dump(exclude_unset=True).items():
        setattr(db_song, key, value)
    db.commit()
    return {"detail": "Song successfully modified"}

@router.post("/api/album/{album_id}/song", tags=["Song"], status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
async def create_song(album_id: int, song: SongBase, db: db_dependency, user_auth: user_dependency):
    # Logged JWT Token validation and user permisions
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

@router.get("/{song_id}", tags=["Song"], status_code=status.HTTP_200_OK)
async def get_song(song_id: int, db: db_dependency, user_auth: user_dependency):
    if user_auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@router.get("/all", tags=["Song"], status_code=status.HTTP_200_OK, response_model=List[SongBase])
async def get_song(db: db_dependency, user_auth: user_dependency):
    if user_auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    songs = db.query(models.Song).all()
    if songs is None:
        raise HTTPException(status_code=404, detail="Songs not found")
    return songs