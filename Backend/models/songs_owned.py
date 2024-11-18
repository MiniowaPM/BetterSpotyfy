from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..db import Base

class Songs_owned(Base):
    __tablename__ = 'songs_owned'
      
    id = Column(Integer, primary_key=True, index=True)
    song_fk = Column(Integer, ForeignKey('songs.id'))
    user_fk = Column(Integer, ForeignKey('users.id'))
    create_date = Column(DateTime(timezone=True), server_default=func.now())
