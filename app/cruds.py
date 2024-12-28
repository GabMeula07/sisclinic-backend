from http import HTTPStatus

from fastapi import HTTPException
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