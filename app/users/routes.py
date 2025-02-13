from http import HTTPStatus

from fastapi import APIRouter, Depends, Form, Query, HTTPException
from sqlalchemy.orm import Session

from typing import List, Dict
from datetime import datetime

from app.config.database import get_session
from app.users.controllers import (
    create_professional_profile_controller,
    create_user_controller,
    creating_schedule_controller,
    delete_user_scheduler_controller,
    get_all_scheduled_controller,
    get_professional_profile_controller,
    get_user_scheduled_controller,
    login_user_controller,
    get_times_by_date_controller
)
from app.users.schemas import (
    ProfileSchema,
    ScheduledAdminListSchema,
    SchedulerListSchema,
    SchedulerRequestSchema,
    TokenSchema,
    UserPublic,
    UserSchema,
)
from app.users.security import (
    get_current_user,
)

user_routes = APIRouter()
# register endpoint


@user_routes.post(
    "/user/",
    tags=["User"],
    response_model=UserPublic,
    status_code=HTTPStatus.CREATED,
)
def register_user(
    user: UserSchema, db_session: Session = Depends(get_session)
):
    return create_user_controller(session=db_session, user=user)


@user_routes.post("/token", tags=["User"], response_model=TokenSchema)
async def login_user(
    username: str = Form(...),
    password: str = Form(...),
    db_session: Session = Depends(get_session),
):
    result = login_user_controller(
        username=username, password=password, session=db_session
    )
    return result


@user_routes.get("/users/profile", tags=["User"], response_model=ProfileSchema)
def get_professional_profile(
    db_session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    profile = get_professional_profile_controller(
        session=db_session, current_user=current_user
    )
    return profile


@user_routes.post(
    "/users/profile", tags=["User"], response_model=ProfileSchema
)
def create_professional_profile(
    data: ProfileSchema,
    db_session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    profile = create_professional_profile_controller(
        session=db_session, current_user=current_user, data=data
    )
    return profile


@user_routes.get("/users/me", tags=["User"], response_model=UserPublic)
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user


""" @user_routes.post("/password-reset-request")
def password_reset_request(
    request: PasswordResetRequest, db_session: Session = Depends(get_session)
):
    return password_reset_request_controller(
        request=request, session=db_session
    )


@user_routes.post("/password-reset")
def password_reset(
    request: PasswordResetConfirm, db_session: Session = Depends(get_session)
):
    password_reset_controller(request=request, session=db_session)
"""


@user_routes.post(
    "/rooms", tags=["Scheduler"], response_model=SchedulerListSchema
)
def rooms_scheduler(
    json: SchedulerRequestSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    response = creating_schedule_controller(
        data=json, session=session, current_user=current_user
    )
    return response


@user_routes.get(
    "/rooms", tags=["Scheduler"], response_model=ScheduledAdminListSchema
)
def get_scheduled_rooms(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
    index: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
):
    return get_all_scheduled_controller(
        session=session,
        current_user=current_user,
        index=index,
        limit=limit,
    )


@user_routes.get(
    "/myrooms", tags=["Scheduler"], response_model=ScheduledAdminListSchema
)
def get_my_scheduled_rooms(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
    index: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
):
    return get_user_scheduled_controller(
        session=session,
        current_user=current_user,
        index=index,
        limit=limit,
    )


@user_routes.delete(
    "/myrooms", tags=["Scheduler"], response_model=SchedulerListSchema
)
async def delete_scheduler(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
    item_id: int = Query(..., gt=0),
):
    data = delete_user_scheduler_controller(
        session=session,
        current_user_id=int(current_user.id),
        scheduler_id=int(item_id),
    )

    return {"scheduled": [data], "msg": "deleted"}



@user_routes.get("/available-times/")
def available_times(target_date: str, db: Session = Depends(get_session), current_user = Depends(get_current_user)) -> Dict[str, List[str]]:
    try:
        # Converte a string para um objeto datetime
        target_date = datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Data inválida. Formato esperado: YYYY-MM-DD")
    
    available_rooms = get_times_by_date_controller(db, target_date)

    if not available_rooms:
        raise HTTPException(status_code=404, detail="Nenhum horário disponível encontrado para a data informada")

    return available_rooms