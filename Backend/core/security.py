from passlib.context import CryptContext
from datetime import timedelta
from ..api.dependencies.auth import create_access_token, authenticate_user
from fastapi import HTTPException, status
from .config import settings

# Settings and constants
minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency for authenticating user and creating an access token
def authenticate_and_create_token(username: str, password: str, db):
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    expires_delta = timedelta(minutes)
    token = create_access_token(username=user.username, user_id=user.id, is_admin=user.is_admin, expires_delta=expires_delta)
    
    return token