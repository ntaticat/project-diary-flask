# Project Diary Flask

## Run App
```[bash]
# Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```
Production
```[bash]
gunicorn -b :8080 wsgi:app
```

## Environment variables needed (.env file)
```[python]
FLASK_ENV="development"
DATABASE_URI="sqlite:///db.sqlite3"
JWT_SECRET="ultra-secret-key"
```