import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Support multiple env names for the database connection string.
    # If you're using Supabase, set `DATABASE_URL` or `SUPABASE_DB_URL` in your .env
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or os.environ.get('SUPABASE_DB_URL')
        or os.environ.get('SQLALCHEMY_DATABASE_URI')
        or 'sqlite:///app.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    # Optional: tune engine options for production Postgres (Supabase)
    # Example: set POOL_SIZE and MAX_OVERFLOW as env vars if needed
    try:
        POOL_SIZE = int(os.environ.get('SQLALCHEMY_POOL_SIZE', 5))
        MAX_OVERFLOW = int(os.environ.get('SQLALCHEMY_MAX_OVERFLOW', 10))
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': POOL_SIZE,
            'max_overflow': MAX_OVERFLOW,
            'pool_pre_ping': True,
        }
    except Exception:
        SQLALCHEMY_ENGINE_OPTIONS = {}
