from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
