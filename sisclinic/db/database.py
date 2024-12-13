import os
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import Session

# Carregando as variáveis de ambiente
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")

# Criando a URL com make_url
db_params = {
    "drivername": "postgresql+psycopg2",  # Corrija o driver para o correto
    "username": DB_USER,
    "password": DB_PASS,
    "host": DB_HOST,
    "port": DB_PORT,
    "database": DB_NAME,
}

url_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criando a engine
engine = create_engine(url_string)

# Exibindo a URL para fins de debug
print(url_string)

def get_session():
    with Session(engine) as session:
        yield session 