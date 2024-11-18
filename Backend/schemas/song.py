from pydantic import BaseModel

class SongBase(BaseModel):
    title: str
    description: str
    genre: int

class UpdateSongBase(BaseModel):
    title: str | None = None
    description: str | None = None
    genre: int | None = None

class Config:
    orm_mode = True
    use_enum_values = True