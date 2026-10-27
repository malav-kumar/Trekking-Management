
import os

class Config:
    # Read the secret key from Render's environment variables.
    SECRET_KEY = os.environ.get("SECRET_KEY", "local-development-key-change-me")

    # Use a persistent disk path if configured on Render.
    # Otherwise, use the default SQLite location for local development.
    DATABASE_PATH = os.environ.get("DATABASE_PATH")

    if DATABASE_PATH:
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE_PATH
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///trekking.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
