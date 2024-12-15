from fastapi import APIRouter, Depends
from sisclinic.utils.services.segurity import get_password_hash
from sqlalchemy import select
from sisclinic.db.database import get_session
from sisclinic.schemas.UserSchemas import UserSchema, UserPublic
from sisclinic.models.models import User
from fastapi import HTTPException
from http import HTTPStatus

user_routes = APIRouter(prefix='/user')

@user_routes.post('/register', response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            User.email == user.email
        )
    )
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email already exists'
        )

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=get_password_hash(user.password)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user