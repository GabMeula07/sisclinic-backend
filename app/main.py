import sys

sys.path.append("/home/gabrielmeula/projects/sisclinic_simplified")

from http import HTTPStatus

from fastapi import Depends, FastAPI, Form
from sqlalchemy.orm import Session

from app.controllers import (
    create_professional_profile_controller,
    create_user_controller,
    get_professional_profile_controller,
    login_user_controller,
    password_reset_controller,
    password_reset_request_controller,
)
from app.database import get_session
from app.schemas import (
    PasswordResetConfirm,
    PasswordResetRequest,
    ProfileSchema,
    TokenSchema,
    UserPublic,
    UserSchema,
)
from app.security import (
    get_current_user,
)

app = FastAPI()


# register endpoint
@app.post("/user/", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def register_user(
    user: UserSchema, db_session: Session = Depends(get_session)
):
    return create_user_controller(session=db_session, user=user)


@app.post("/token", response_model=TokenSchema)
async def login_user(
    username: str = Form(...),
    password: str = Form(...),
    db_session: Session = Depends(get_session),
):
    result = login_user_controller(
        username=username, password=password, session=db_session
    )
    return result


@app.get("/users/profile", response_model=ProfileSchema)
def get_professional_profile(
    db_session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    profile = get_professional_profile_controller(
        session=db_session, current_user=current_user
    )
    return profile


@app.post("/users/profile", response_model=ProfileSchema)
def create_professional_profile(
    data: ProfileSchema,
    db_session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    profile = create_professional_profile_controller(
        session=db_session, current_user=current_user, data=data
    )
    return profile


@app.get("/users/me", response_model=UserPublic)
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user


@app.post("/password-reset-request")
def password_reset_request(
    request: PasswordResetRequest, db_session: Session = Depends(get_session)
):
    return password_reset_request_controller(
        request=request, session=db_session
    )


@app.post("/password-reset")
def password_reset(
    request: PasswordResetConfirm, db_session: Session = Depends(get_session)
):
    password_reset_controller(request=request, session=db_session)
