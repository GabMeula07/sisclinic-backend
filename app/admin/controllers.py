from sqlalchemy.orm import Session

from app.admin.cruds import get_all_user, get_all_user_data
from app.admin.services import check_admin


def get_all_users_admin_controller(session: Session, current_user):
    check_admin(current_user)
    list_users = get_all_user(session=session)
    return list_users


def get_user_profile(session: Session, current_user, user_id):
    check_admin(current_user)
    user_profile = get_all_user_data(session=session, user_id=user_id)
    return user_profile
