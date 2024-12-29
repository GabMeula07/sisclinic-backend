import sys

sys.path.append("/home/gabrielmeula/projects/sisclinic_simplified")

from http import HTTPStatus

from fastapi import Depends, FastAPI, Form, HTTPException
from sqlalchemy.orm import Session

from app.cruds import create_user, get_user_by_email
from app.database import get_session
from app.schemas import UserPublic, UserSchema
from app.security import create_access_token, get_current_user, verify_password

app = FastAPI()


# register endpoint
@app.post("/user/", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def post_user(user: UserSchema, db_session: Session = Depends(get_session)):
    db_user = create_user(session=db_session, user=user)
    return db_user


@app.post("/token")
async def login_user(
    username: str = Form(...),
    password: str = Form(...),
    db_session: Session = Depends(get_session),
):
    user = get_user_by_email(session=db_session, email=username)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid Email or Password",
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid Email or Password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
