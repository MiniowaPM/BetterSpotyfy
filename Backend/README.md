1. Install python, pip
2. Create a virtual environment 
    python -m venv .env
3. Activate the virtual environment
    .\Backend\.env\Scripts\activate
4. Install packages
    pip install fastapi uvicorn sqlalchemy pymysql "python-jose[cryptography]" "passlib[bcrypt]" python-multipart 
5. Start the app via uvicorn
    uvicorn Backend.main:app --reload
    python -m uvicorn app.main:app --relaod
6. Install XAMPP, and establish connection via database.py