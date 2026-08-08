# This class stores all the configuration settings
class Config:

    # Secret key used by Flask to secure session data
    # (for example, when a user logs in).
    SECRET_KEY = "trek123"

    # Database location.
    # We are using SQLite, and the database file
    # will be named 'trekking.db'.
    SQLALCHEMY_DATABASE_URI = "sqlite:///trekking.db"

    # Disable modification tracking because
    # our project doesn't need it.
    # This also removes unnecessary warning messages.
    SQLALCHEMY_TRACK_MODIFICATIONS = False