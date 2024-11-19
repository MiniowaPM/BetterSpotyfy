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

## About the Project ##

> This FastAPI-based REST API provides endpoints to handle save and secure connection to database, user authenticaton via JSON Web Token (JWT), database injection based on user permision via HTTP methods. It is optimized for performance, provides detailed API documentation, and follows best practices for API development.

## Features ##
- CRUD operations for managing resources.
- JWT-based authentication and authorization.
- Validation of request data using Pydantic.
- OpenAPI documentation available at /docs.
- Integration-ready with databases (MySQL).

## Tech Stack ##

- Framework: FastAPI
- Language: Python 3.8+
- Database: MySQL (SQLAlchemy)
- Authentication: JWT
- Encription: Bcrypt
- Other Tools: Uvicorn, Pydantic

## Getting Started ##

Follow these instructions to set up the project locally.

### Prerequisites ###
- Python 3.8 or higher
- Pipenv

### Installation ###

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

``` DB_USER = "database_user" ```

``` DB_PASSWORD = "database_user_password" ```

``` DB_NAME = "database_name" ```

``` SECRET_KEY = " your_secret_key" ```

5. Run the MySQL database:

Open database menagment system (eg. XAMPP):

``` Create database database_name ```

``` CREATE USER 'database_user' IDENTIFIED BY 'database_user_password'; ```

``` GRANT ALL PRIVILEGES ON database_name.* TO 'database_user'; ```

``` FLUSH PRIVILAGES; ```

7. Start the development server:

```uvicorn app.main:app --reload```

## API Endpoints ##

Base URL: http://localhost:8000

### User Endpoints ###

| Method | Endpoint            | Description                  | Auth Required              |
|--------|---------------------|------------------------------|----------------------------|
| POST   | /user/             | Sign-up user                | No                         |
| PATCH  | /user/{user_id}    | Update user                 | JWT Token + is_admin       |
| PATCH  | /user/me           | Update logged user          | JWT Token                  |
| DELETE | /user/{user_id}    | Delete user                 | JWT Token + is_admin       |
| GET    | /user/{user_id}    | Get partial user info       | JWT Token                  |
| GET    | /user/me           | Get all logged user info    | JWT Token                  |
| GET    | /user/all          | Get partial users info      | JWT Token + is_admin       |
| GET    | /user/all          | Get users info              | JWT Token + is_admin       |

#### Album Endpoints ####

| Method | Endpoint              | Description                     | Auth Required              |
|--------|-----------------------|---------------------------------|----------------------------|
| POST   | /albums/             | Add a new album                | JWT Token + is_admin       |
| GET    | /albums/             | Get all albums                 | No                         |
| GET    | /albums/{album_id}   | Get album details by ID        | No                         |
| PATCH  | /albums/{album_id}   | Update album details           | JWT Token + is_admin       |
| DELETE | /albums/{album_id}   | Delete album                   | JWT Token + is_admin       |


#### Song Endpoint ####

| Method | Endpoint              | Description                     | Auth Required              |
|--------|-----------------------|---------------------------------|----------------------------|
| POST   | /songs/              | Add a new song                 | JWT Token + is_admin       |
| GET    | /songs/              | Get all songs                  | No                         |
| GET    | /songs/{song_id}     | Get song details by ID         | No                         |
| PATCH  | /songs/{song_id}     | Update song details            | JWT Token + is_admin       |
| DELETE | /songs/{song_id}     | Delete song                    | JWT Token + is_admin       |

#### Other Endpoints ####

| Method | Endpoint              | Description                     | Auth Required              |
|--------|-----------------------|---------------------------------|----------------------------|
| GET    | /                     | Welcome page                   | JWT Token + is_admin       |
| GET    | /auth/token           | Login and get access token     | No                         |


Detailed documentation and interactive API docs available at /docs (Swagger UI).

## Contact ##

Name: Miniowa

Email: 31001@s.pm.szczecin.pl

GitHub: @MiniowaPM

