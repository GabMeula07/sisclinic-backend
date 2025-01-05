from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_, func, select, extract

from app.models import ProfessionalRecord, Schedule, User
from app.security import get_password_hash


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
        session: Session, 
        date_scheduled, 
        time_scheduled, 
        room
    ):
    db_schedule = session.scalar(
        select(Schedule).where(
            and_(
                Schedule.room == room,
                Schedule.time_scheduled == time_scheduled,
                extract('dow',Schedule.date_scheduled) == extract('dow',date_scheduled),
                Schedule.active == True
            )
        )
    )  
    if db_schedule:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='this scheduler is fixed'
        )


def create_schedule(data: dict, session: Session, current_user):
    db_schedule = session.scalar(
        select(Schedule).where(
            and_(
                Schedule.room == data.room,
                Schedule.time_scheduled == data.time_scheduled,
                Schedule.date_scheduled == data.date_scheduled,
            )
        )
    )

    if db_schedule:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Schedule already exists",
        )
    
    check_fixed_scheduled(
        session=session,
        date_scheduled=data.date_scheduled,
        time_scheduled=data.time_scheduled,
        room=data.room
    )


    db_schedule = Schedule(
        user_id=current_user.id,
        room=data.room,
        date_scheduled=data.date_scheduled,
        time_scheduled=data.time_scheduled,
        type_scheduled=data.type_scheduled,
    )

    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)

    return db_schedule


def get_schedule(session: Session, index=None, limit=None):
    result = session.scalars(
        select(Schedule)
        .where(Schedule.date_scheduled >= datetime.now())
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
                Schedule.date_scheduled >= datetime.now(),
                Schedule.user_id == user_id,
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
