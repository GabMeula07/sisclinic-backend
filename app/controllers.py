import sys

sys.path.append("/home/gabrielmeula/projects/sisclinic_simplified")

from http import HTTPStatus

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.cruds import (
    create_professional,
    create_user,
    get_professional,
    get_user_by_email,
    update_user,
    create_schedule
)
from app.schemas import (
    PasswordResetConfirm,
    PasswordResetRequest,
    ProfileSchema,
)
from app.security import (
    create_access_token,
    create_reset_token,
    verify_password,
    verify_reset_token,
)
from app.services import send_reset_email

# User Controllers


def create_user_controller(user: dict, session: Session):
    db_user = create_user(session=session, user=user)
    return db_user


def login_user_controller(
    username: str,
    password: str,
    session: Session,
):
    user = get_user_by_email(session=session, email=username)
    if user is None or not verify_password(password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid Email or Password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def read_current_user_controller(current_user):
    return current_user


# Profile Controllers


def get_professional_profile_controller(
    session: Session,
    current_user,
):
    profile = get_professional(session, current_user)
    return profile


def create_professional_profile_controller(
    session: Session,
    current_user,
    data: ProfileSchema,
):
    profile = create_professional(
        session=session, user=current_user, data=data
    )
    return profile


# Password Reset Controllers


def password_reset_request_controller(
    request: PasswordResetRequest, session: Session
):
    user = get_user_by_email(session=session, email=request.email)
    token = create_reset_token({"sub": user.email})
    send_reset_email(user.email, token)

    return {"message": "Token sent to the provided email address"}


def password_reset_controller(request: PasswordResetConfirm, session: Session):
    # Verify token
    email = verify_reset_token(request.token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )

    # Update password
    user = get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    update_user(
        session=session, user=user, data={"password": request.new_password}
    )

    return {"message": "Password successfully updated"}


def creating_schedule_controller(
    data: dict, session: Session, current_user
): 
    scheduled = create_schedule(data=data, session=session, current_user=current_user)
    return{
        "scheduled": [scheduled],
        "msg": "OK"
    }
