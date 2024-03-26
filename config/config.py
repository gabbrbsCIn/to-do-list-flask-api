import os
from dotenv import load_dotenv
load_dotenv()

def get_db_uri():
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    host = os.environ.get("DB_HOST")
    database = os.environ.get("DB_DATABASE")
    port = os.environ.get("DB_PORT")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

SECRET_KEY = os.environ.get("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = get_db_uri()
SQLALCHEMY_TRACK_MODIFICATIONS = False
