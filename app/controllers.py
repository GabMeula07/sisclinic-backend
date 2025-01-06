import sys

sys.path.append("/home/gabrielmeula/projects/sisclinic_simplified")

from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.cruds import (
    create_professional,
    create_schedule,
    create_user,
    get_max_index,
    get_max_index_by_user_id,
    get_professional,
    get_schedule,
    get_scheduler_by_user_id,
    get_user_by_email,
    get_scheduler_by_id,
    delete_user_scheduler,
)
from app.schemas import (
    ProfileSchema,
)
from app.security import (
    create_access_token,
    verify_password,
)

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


""" def password_reset_request_controller(
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
 """

# Scheduler Controllers


def creating_schedule_controller(data: dict, session: Session, current_user):
    if not current_user.is_active:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="User is not active"
        )

    scheduled = create_schedule(
        data=data, session=session, current_user=current_user
    )
    return {"scheduled": [scheduled], "msg": "OK"}


def get_all_scheduled_controller(
    session: Session, current_user, index=0, limit=10
):
    if not current_user.is_adm:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="User is not adm"
        )

    scheduled = get_schedule(session=session, index=index, limit=limit)
    data = {
        "prox_index": (index + limit + 1)
        if (index + limit) < get_max_index(session=session)
        else None,
        "max_index": int(get_max_index(session=session)),
        "scheduled": scheduled,
    }
    return data


def get_user_scheduled_controller(
    session: Session, current_user, index=0, limit=10
):
    scheduled = get_scheduler_by_user_id(
        session=session, user_id=int(current_user.id), index=index, limit=limit
    )

    data = {
        "prox_index": (index + limit + 1)
        if (index + limit) < get_max_index(session=session)
        else None,
        "max_index": int(
            get_max_index_by_user_id(
                session=session, user_id=int(current_user.id)
            )
        ),
        "scheduled": scheduled,
    }

    return data


def delete_user_scheduler_controller(
    session: Session, scheduler_id: int, current_user_id: int
):  
    scheduler = get_scheduler_by_id(session=session, scheduler_id=scheduler_id)
    data = delete_user_scheduler(
        session=session, 
        current_user_id=current_user_id,
        schedule=scheduler
    )
    return data