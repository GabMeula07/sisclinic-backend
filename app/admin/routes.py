from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.admin.controllers import (
    closing_fixed_month_controller,
    closing_of_the_month_controller,
    get_all_scheduler_controller,
    get_all_users_admin_controller,
    get_sheduler_user_data_controller,
    get_user_profile,
)
from app.admin.schemas import (
    AllUserAdmin,
    SchedulerListAdmin,
    UserProfileAdmin,
)
from app.admin.services import check_admin
from app.config.database import get_session
from app.users.security import get_current_user

admin_routes = APIRouter(
    prefix="/admin", dependencies=[Depends(get_current_user)]
)


@admin_routes.get("/")
def hello_world(current_user=Depends(get_current_user)):
    check_admin(current_user)
    return {"msg": "Hello Admin"}


@admin_routes.get("/users/", response_model=AllUserAdmin)
def get_all_users(
    session=Depends(get_session), current_user=Depends(get_current_user)
):
    list_users = get_all_users_admin_controller(
        session=session, current_user=current_user
    )
    return {"users_list": list_users}


@admin_routes.get("/users/{user_id}", response_model=UserProfileAdmin)
def get_profile_user(
    user_id: int,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
):
    profile = get_user_profile(
        session=session, current_user=current_user, user_id=user_id
    )
    return profile


@admin_routes.get(
    "/users/{user_id}/shedulers/", response_model=SchedulerListAdmin
)
def get_user_sheduler(
    user_id: int,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
):
    return get_sheduler_user_data_controller(
        session=session,
        current_user=current_user,
        user_id=user_id,
        offset=offset,
        limit=limit,
    )


@admin_routes.get("/scheduler/", response_model=SchedulerListAdmin)
def get_all_scheduler_events(
    session=Depends(get_session),
    current_user=Depends(get_current_user),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    data_min: str = Query(None),
    data_max: str = Query(None),
):
    schedulers = get_all_scheduler_controller(
        current_user=current_user,
        session=session,
        offset=offset,
        limit=limit,
        data_min=data_min,
        data_max=data_max,
    )
    return schedulers


@admin_routes.get("/closing/month/{user_id}")
def closing_of_the_month(
    user_id: int,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
    month: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
):
    return closing_of_the_month_controller(
        session, current_user, user_id, month, year
    )


@admin_routes.get("/closing/month1/{user_id}")
def closing_of_the_month(
    user_id: int,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
    month: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
):
    return closing_fixed_month_controller(
        session, current_user, user_id, month, year
    )
