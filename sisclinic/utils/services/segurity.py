import os
from pwdlib import PasswordHash
from dotenv import load_dotenv

load_dotenv('/home/gabrielmeula/projects/sisclinic/.env')

pwd_context = PasswordHash.recommended()

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = 'HS256'

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)