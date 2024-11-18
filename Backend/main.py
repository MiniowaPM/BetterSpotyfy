from fastapi import FastAPI
from Backend.api.routes import auth_router, user_router, album_router, song_router
from Backend.db import engine, Base

# Create instance of an FastApi app
app = FastAPI()

# Include API routers
app.include_router(user_router)
app.include_router(album_router)
app.include_router(song_router)
app.include_router(auth_router)


# Initialize and create the database tables
Base.metadata.create_all(bind=engine)

# Default route
@app.get("/")
def Deafault():
    return {"message": "Welcome to the FastAPI app!"}