from datetime import datetime, timezone
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_, extract, func, select

from app.config.models import (
    ProfessionalRecord,
    Schedule,
    ScheduleDeactivation,
    User,
)
from app.users.security import get_password_hash


def create_user(session: Session, user: dict):
    db_user = session.scalar(select(User).where(User.email == user.email))
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Email already exists"
        )

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(session: Session, email: str):
    db_user = session.scalar(select(User).where(User.email == email))
    return db_user


def update_user(session: Session, user: User, data: dict):
    for key, value in data.items():
        if key == "password":
            setattr(user, key, get_password_hash(value))
        else:
            setattr(user, key, value)

    session.commit()
    session.refresh(user)
    return user


def create_professional(session: Session, user, data: dict):
    db_profile = session.scalar(
        select(ProfessionalRecord).where(ProfessionalRecord.user_id == user.id)
    )

    if db_profile:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Profile already exists"
        )

    db_profile = ProfessionalRecord(
        user_id=user.id,
        birth=data.birth,
        cpf=data.cpf,
        occupation=data.occupation,
        specialization=data.specialization,
        number_record=data.number_record,
        street=data.street,
        number=data.number,
        not_number=data.not_number,
        neighborhood=data.neighborhood,
        city=data.city,
        cep=data.cep,
    )
    update_user(session, user, {"is_active": True})

    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)

    return db_profile


def get_professional(session: Session, user):
    db_profile = session.scalar(
        select(ProfessionalRecord).where(ProfessionalRecord.user_id == user.id)
    )
    if not db_profile:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Profile User not Found"
        )
    return db_profile


def check_fixed_scheduled(
    session: Session, date_scheduled, time_scheduled, room
):
    db_schedule = session.scalar(
        select(Schedule).where(
            and_(
                Schedule.room == room,
                Schedule.time_scheduled == time_scheduled,
                extract("dow", Schedule.date_scheduled)
                == extract("dow", date_scheduled),
                Schedule.active == True,
            )
        )
    )
    if db_schedule:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="this scheduler is fixed",
        )


def check_scheduler_deactivate(session: Session, scheduler, current_user):
    query = (
        select(ScheduleDeactivation)
        .join(Schedule, ScheduleDeactivation.schedule_id == Schedule.id)
        .filter(
            ScheduleDeactivation.user_id == int(current_user.id),
            ScheduleDeactivation.date_limit >= datetime.now(timezone.utc),
            Schedule.room == scheduler.room,
            Schedule.time_scheduled == scheduler.time_scheduled,
            extract("dow", Schedule.date_scheduled)
            == extract("dow", scheduler.date_scheduled),
        )
    )

    result = session.execute(query).scalars().first()

    if result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="You Cant Scheduled this room",
        )


def create_schedule(data: dict, session: Session, current_user):
    db_schedule = session.scalar(
        select(Schedule).where(
            and_(
                Schedule.room == data.room,
                Schedule.time_scheduled == data.time_scheduled,
                Schedule.date_scheduled == data.date_scheduled,
                Schedule.active == True,
            )
        )
    )

    if db_schedule:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Schedule already exists",
        )

    check_scheduler_deactivate(
        session=session, scheduler=data, current_user=current_user
    )

    check_fixed_scheduled(
        session=session,
        date_scheduled=data.date_scheduled,
        time_scheduled=data.time_scheduled,
        room=data.room,
    )

    db_schedule = Schedule(
        user_id=current_user.id,
        room=data.room,
        date_scheduled=data.date_scheduled,
        time_scheduled=data.time_scheduled,
        is_fixed=data.is_fixed,
    )

    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)

    return db_schedule


def get_schedule(session: Session, index=None, limit=None):
    result = session.scalars(
        select(Schedule)
        .where(Schedule.date_scheduled >= datetime.now(timezone.utc))
        .offset(index)
        .limit(limit)
    )
    return list(result)


def get_scheduler_by_user_id(
    session: Session, user_id: int, index=None, limit=None
):
    result = session.scalars(
        select(Schedule)
        .where(
            and_(
                Schedule.date_scheduled >= datetime.now(timezone.utc).date(),
                Schedule.user_id == user_id,
                Schedule.active == True,
            )
        )
        .offset(index)
        .limit(limit)
    )
    return list(result)


def get_max_index(session: Session):
    today = datetime.today()
    max_index = (
        session.query(func.count(Schedule.id))
        .filter(Schedule.date_scheduled >= today)
        .scalar()
    )
    return max_index


def get_max_index_by_user_id(session: Session, user_id: int):
    today = datetime.today()
    max_index = (
        session.query(func.count(Schedule.id))
        .filter(Schedule.date_scheduled >= today, Schedule.user_id == user_id)
        .scalar()
    )
    return max_index


def delete_user_scheduler(
    session: Session, schedule: Schedule, current_user_id
):
    if schedule.is_fixed:
        create_scheduler_deactivate(
            session=session, schedule=schedule, current_user_id=current_user_id
        )

    setattr(schedule, "active", False)
    session.commit()
    session.refresh(schedule)
    return schedule


def create_scheduler_deactivate(
    session: Session, schedule: Schedule, current_user_id
):
    schedule_deactivate = ScheduleDeactivation(
        user_id=current_user_id, schedule_id=schedule.id
    )
    session.add(schedule_deactivate)
    session.commit()
    session.refresh(schedule_deactivate)

    return schedule_deactivate


def get_scheduler_by_id(session: Session, scheduler_id: int):
    scheduler = session.scalar(
        select(Schedule).where(Schedule.id == scheduler_id)
    )
    if not scheduler_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Scheduler not found"
        )

    return scheduler
