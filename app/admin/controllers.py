from datetime import datetime

from sqlalchemy.orm import Session

from app.admin.cruds import (
    clean_group_date,
    clising_month_by_extra,
    closing_fixed_month,
    get_all_schedulers,
    get_all_user,
    get_all_user_data,
    get_dates_with_same_weekday,
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


def closing_of_the_month_controller(
    session, current_user, user_id, month, year
):
    check_admin(current_user=current_user)

    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year

    result = closing_fixed_month(
        session=session, user_id=user_id, month=month, year=year
    )

    data = {}
    fixo_detail = []

    for scheduler in result:
        data_temp = {}
        data_temp["id"] = scheduler.id
        data_temp["date_fixed"] = scheduler.date_scheduled
        data_temp["ativo"] = scheduler.active
        data_temp["dates_generate"] = get_dates_with_same_weekday(
            scheduler.date_scheduled, month=month, year=year
        )
        if not scheduler.active:
            data_temp["dates_generate"] = clean_group_date(
                session=session, user_id=user_id, scheduler=data_temp
            )

        fixo_detail.append(data_temp)

    
    data["extra"] = clising_month_by_extra(
            session=session, user_id=user_id, month=month, year=year
        )
    
    total_value = 0
    for _dict in fixo_detail:
        total_value += (len(_dict["dates_generate"])*25)

    fixo = {
        "total_fixos": len(result),
        "total_value": total_value,
        "detail": fixo_detail
    }
    data["fixo"] = fixo
    
    return data


def closing_fixed_month_controller(
    session, current_user, user_id, month, year
):
    check_admin(current_user=current_user)

    if month is None:
        month = datetime.now().month
    if year is None:
        year = datetime.now().year

    result = closing_fixed_month(
        session=session, user_id=user_id, month=month, year=year
    )

    data = []

    for scheduler in result:
        data_temp = {}
        data_temp["id"] = scheduler.id
        data_temp["date_fixed"] = scheduler.date_scheduled
        data_temp["ativo"] = scheduler.active
        data_temp["dates_generate"] = get_dates_with_same_weekday(
            scheduler.date_scheduled, month=month, year=year
        )
        if not scheduler.active:
            data_temp["dates_generate"] = clean_group_date(
                session=session, user_id=user_id, scheduler=data_temp
            )

        data.append(data_temp)

    return data
