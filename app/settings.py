from decouple import config

SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")
