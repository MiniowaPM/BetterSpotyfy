DB_USER = "API_ADMIN"
DB_PASSWORD = "password123"
DB_NAME = "TEST_API"

class Settings:
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_NAME}"
    SECRET_KEY: str = "default_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()