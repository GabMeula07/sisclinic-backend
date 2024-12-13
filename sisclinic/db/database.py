import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, make_url
from sqlalchemy.orm import Session

load_dotenv("/home/gabrielmeula/projects/sisclinic/.env")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")

url = make_url(
    {
        "drivename": "postgresql+pyscopg2",
        "username": DB_USER,
        "password": DB_PASS,
        "host": DB_HOST,
        "port": DB_PORT,
        "database": DB_NAME,
    }
)
engine = create_engine(url)


def get_session():
    with Session(engine) as session:
        yield session
