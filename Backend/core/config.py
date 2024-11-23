DATABASES = {
    "MySQL": "mysql+pymysql",
    "SQLite": "SQLite",
    "Postgresql": "postgresql",
    "Oracle": "oracle+oracledb",
    "Microsoft SQL": "mssql+pyodbc"
}

SELECTED_DB = "MySQL"
DB_USER = "API_ADMIN"
DB_PASSWORD = "password123"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "TEST_API"

class Settings:
    if DATABASES == "SQLite":
        DATABASE_URL: str = "sqlite:///database.db"
    else:
        DATABASE_URL: str = f"{DATABASES.get(SELECTED_DB)}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SECRET_KEY: str = "default_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()