from sqlalchemy.orm import Session

from app.admin.cruds import (
    get_all_schedulers,
    get_all_user,
    get_all_user_data,
    get_scheduler_user,
)
from app.admin.services import check_admin


def get_all_users_admin_controller(session: Session, current_user):
    check_admin(current_user)
    list_users = get_all_user(session=session)
    return list_users


def get_user_profile(session: Session, current_user, user_id):
    check_admin(current_user)
    user_profile = get_all_user_data(session=session, user_id=user_id)
    return user_profile


def get_sheduler_user_data_controller(
    session: Session, current_user, user_id: int, offset: int, limit: int
):
    check_admin(current_user)
    return get_scheduler_user(
        session=session, user_id=user_id, offset=offset, limit=limit
    )


def get_all_scheduler_controller(
    session, current_user, offset, limit, data_min, data_max
):
    check_admin(current_user=current_user)
    schedulers = get_all_schedulers(
        session=session,
        offset=offset,
        limit=limit,
        data_min=data_min,
        data_max=data_max,
    )
    return schedulers
