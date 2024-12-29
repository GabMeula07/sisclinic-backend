from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from app.models import User
from app.security import get_password_hash


def create_user(session, user):
    db_user = session.scalar(select(User).where(User.email == user.email))
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Email already exists"
        )

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(session: Session, email: str):
    db_user = session.scalar(select(User).where(User.email == email))
    return db_user

def update_user(session: Session, user: User, data: dict):
    for key, value in data.items():
        if key == 'password':
            setattr(user, key, get_password_hash(value))
        else: 
            setattr(user, key, value)

    session.commit()
    session.refresh(user)
    return user    

