DATABASES = {
    1: "MySQL",
    2: "SQLite",
    3: "Postgresql"
}

DATABASES = 1
DB_USER = "API_ADMIN"
DB_PASSWORD = "password123"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "TEST_API"

class Settings:
    if DATABASES == 1:
        DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    if DATABASES == 2:
        DATABASE_URL: str = "sqlite:///database.db"
    if DATABASES == 3:
        DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        DATABASE_URL: None
    SECRET_KEY: str = "default_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()