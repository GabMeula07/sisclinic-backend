from fastapi import APIRouter, Depends, Query

from app.admin.controllers import (
    get_all_users_admin_controller,
    get_sheduler_user_data,
    get_user_profile,
)
from app.admin.schemas import AllUserAdmin, UserProfileAdmin
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


@admin_routes.get("/users/{user_id}/shedulers/")
def get_user_sheduler(
    user_id: int,
    session=Depends(get_session),
    current_user=Depends(get_current_user),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
):
    list_scheduled = get_sheduler_user_data(
        session=session,
        current_user=current_user,
        user_id=user_id,
        offset=offset,
        limit=limit,
    )
    return {
        "scheduled": list_scheduled
    }