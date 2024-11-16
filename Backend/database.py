from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_USER = "API_ADMIN"
DB_PASSWORD = "password123"
DB_NAME = "TEST_API"

URL_DATABASE = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_NAME}"

# URL_DATABASE = 'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/BetterSpotifyDB'
# URL_DATABASE = 'mysql+pymysql://USERNAME:PASSWORD@SERVER_IP:PORT/DB_NAME'

engine = create_engine(URL_DATABASE)
    
SessionLocal = sessionmaker(autocommit=False ,autoflush=False, bind=engine)

Base = declarative_base()