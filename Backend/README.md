# BetterSpotify ⛅ #

> A backend REST API built with FastAPI for handling http requests to database. It is designed to be fast, efficient, and easy to integrate.

## Table of Contents ##
- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Contact](#contact)

## About the Project 📝 ##

> This FastAPI-based REST API provides endpoints to handle save and secure connection to database, user authenticaton via JSON Web Token (JWT), database injection based on user permision via HTTP methods. It is optimized for performance, provides detailed API documentation, and follows best practices for API development.

## Features ✨ ##
- CRUD operations for managing resources.
- JWT-based authentication and authorization.
- Validation of request data using Pydantic.
- OpenAPI documentation available at /docs.
- Integration-ready with databases (MySQL, SQLite, PostgreSQL).

## Tech Stack 🛠️ ##

- Framework: FastAPI
- Language: Python 3.8+
- Database: MySQL (SQLAlchemy)
- Authentication: JWT
- Encription: Bcrypt
- Other Tools: Uvicorn, Pydantic

## Getting Started 🚀 ##

Follow these instructions to set up the project locally.

### Prerequisites 🔧 ###
- Python 3.8 or higher
- Pipenv

### Installation ⚙️ ###

1. Clone the repository:

```git clone https://github.com/MiniowaPM/BetterSpotyfy.git```

```cd BetterSpotify```

2. Create and activate a virtual environment:

```python -m venv .env```

```- source venv/bin/activate```  # For Linux/Mac

```- venv\Scripts\activate```     # For Windows

3. Install dependencies:

```pip install -r requirements.txt```

4. Set up config file in the Backend/core/config.py directory and change setting class values:

```DATABASES = 1 ``` # 1: MySQL, 2: SQLite, 3: PostgreSQL,  4: ...

```DB_USER = "API_ADMIN" ```

```DB_PASSWORD = "password123" ```

```DB_HOST = "localhost" ```

```DB_PORT = "3306" ```

```DB_NAME = "TEST_API" ```

5. Run the MySQL database:

Open database menagment system (eg. XAMPP):

``` Create database database_name ```

``` CREATE USER 'database_user' IDENTIFIED BY 'database_user_password'; ```

``` GRANT ALL PRIVILEGES ON database_name.* TO 'database_user'; ```

``` FLUSH PRIVILAGES; ```

7. Start the development server:

```uvicorn app.main:app --reload```

## API Endpoints 🌐 ##

Base URL: http://localhost:8000

### User Endpoints 📧 ###

| Method | Endpoint           | Description                 | Auth Required              |
|--------|--------------------|-----------------------------|----------------------------|
| POST   | /user/             | Sign-up user                | No                         |
| PATCH  | /user/{user_id}    | Update user                 | JWT Token + is_admin       |
| PATCH  | /user/me           | Update logged user          | JWT Token                  |
| DELETE | /user/{user_id}    | Delete user                 | JWT Token + is_admin       |
| GET    | /user/{user_id}    | Get partial user info       | JWT Token                  |
| GET    | /user/me           | Get all logged user info    | JWT Token                  |
| GET    | /user/all          | Get partial users info      | JWT Token + is_admin       |
| GET    | /user/all          | Get users info              | JWT Token + is_admin       |
| POST   | /user/me/profile-image/ | Uploads user profile image | JWT Token              |
| GET    | /user/{user_id}/profile-image/ | Get user profile image | JWT Token           |

### Album Endpoints ###

| Method | Endpoint             | Description                    | Auth Required              |
|--------|----------------------|--------------------------------|----------------------------|
| POST   | /albums/             | Add a new album                | JWT Token + is_admin       |
| GET    | /albums/             | Get all albums                 | No                         |
| GET    | /albums/{album_id}   | Get album details by ID        | No                         |
| PATCH  | /albums/{album_id}   | Update album details           | JWT Token + is_admin       |
| DELETE | /albums/{album_id}   | Delete album                   | JWT Token + is_admin       |
| POST   | /albums/{user_id}/album-image/ | Uploads album thumbnail image  | JWT Token        |
| GET    | /albums/{user_id}/album-image/ | Get user album thumbnail image | JWT Token        |

### Song Endpoint ###

| Method | Endpoint             | Description                    | Auth Required              |
|--------|----------------------|--------------------------------|----------------------------|
| POST   | /songs/              | Add a new song                 | JWT Token + is_admin       |
| GET    | /songs/              | Get all songs                  | No                         |
| GET    | /songs/{song_id}     | Get song details by ID         | No                         |
| PATCH  | /songs/{song_id}     | Update song details            | JWT Token + is_admin       |
| DELETE | /songs/{song_id}     | Delete song                    | JWT Token + is_admin       |

### Other Endpoints ###

| Method | Endpoint              | Description                    | Auth Required              |
|--------|-----------------------|--------------------------------|----------------------------|
| GET    | /                     | Welcome page                   | No                         |
| GET    | /auth/token           | Login and get access token     | No                         |


### Extra info: ###
> JWT Token is aquired by logging to the database with /auth/token route

> is_admin is condition whether the user accout has record ```is_admin == 1```  

Detailed documentation and interactive API docs available at /docs (Swagger UI).

## Contact ##

Name: Miniowa

Email: 31001@s.pm.szczecin.pl

GitHub: @MiniowaPM