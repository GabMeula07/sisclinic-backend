from datetime import datetime, timezone, date, timedelta
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_, extract, func, select, or_

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


from collections import defaultdict

def get_available_rooms_and_times(session: Session, target_date: datetime): 
    target_date = target_date.date()
    month = target_date.month
    year = target_date.year

    all_possible_times = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
    rooms = [f'Sala {i:02}' for i in range(1, 7)]  
    date_fixed = session.scalars(select(Schedule.date_scheduled).where(
        and_(
            Schedule.active == True, 
            Schedule.is_fixed == True
        )
    )).all()

    dates_generated = set()
    for _date in date_fixed:
        dates_generated.update(get_dates_with_same_weekday(_date, month, year))

    has_fixed_schedules = target_date in dates_generated

    normal_schedules = session.execute(select(Schedule).where(
        and_(
            Schedule.active == True, 
            Schedule.is_fixed == False,
            Schedule.date_scheduled == target_date
        )
    )).scalars().all()

    # Dicionário para armazenar horários ocupados por sala
    schedules_dict = defaultdict(lambda: {"normal": [], "fixed": []})

    # Processar agendamentos normais
    for schedule in normal_schedules:
        schedules_dict[schedule.room]["normal"].append(schedule.time_scheduled)

    # Se há agendamentos fixos para a data, buscar quais são
    if has_fixed_schedules:
        fixed_schedules = session.execute(select(Schedule).where(
            and_(
                Schedule.active == True,
                Schedule.is_fixed == True
            )
        )).scalars().all()

        for schedule in fixed_schedules:
            if schedule.date_scheduled in dates_generated:  # Considerar apenas os fixos na mesma semana/mês
                schedules_dict[schedule.room]["fixed"].append(schedule.time_scheduled)

    # Determinar horários disponíveis por sala
    available_rooms = {}
    for room in rooms:
        occupied_times = schedules_dict[room]["normal"] + schedules_dict[room]["fixed"]
        available_times = [time for time in all_possible_times if time not in occupied_times]

        if available_times:
            available_rooms[room] = available_times

    return available_rooms



def get_dates_with_same_weekday(date: datetime.date, month: int, year: int):
    """
    Retorna todas as datas de um mês e ano fornecidos que têm o mesmo dia da semana da data fornecida.

    Args:
        date (datetime.date): A data de referência para determinar o dia da semana.
        month (int): O mês desejado.
        year (int): O ano desejado.

    Returns:
        list[datetime.date]: Uma lista contendo todas as datas do mês que têm o mesmo dia da semana.
    """
    # Garantir que a data seja um objeto do tipo `datetime.date`
    if isinstance(date, datetime):
        date = date.date()

    # Primeiro dia do mês fornecido
    first_day = datetime(year, month, 1).date()

    # Último dia do mês fornecido
    next_month = (month % 12) + 1
    next_month_year = year + (1 if next_month == 1 else 0)
    last_day = datetime(next_month_year, next_month, 1).date() - timedelta(
        days=1
    )

    # Primeiro dia do mês com o mesmo dia da semana da data fornecida
    first_matching_day = first_day + timedelta(
        days=(date.weekday() - first_day.weekday()) % 7
    )

    # Gera todas as datas com o mesmo dia da semana no mês fornecido
    return [
        first_matching_day + timedelta(weeks=i)
        for i in range((last_day - first_matching_day).days // 7 + 1)
    ]


def closing_fixed_month(session: Session, user_id, month, year):
    now = datetime.now(timezone.utc)

    if month is None:
        month = now.month
    if year is None:
        year = now.year

    first_day = datetime(year, month, 1)
    next_month = (month % 12) + 1
    next_month_year = year + (1 if next_month == 1 else 0)
    last_day = datetime(next_month_year, next_month, 1) - timedelta(days=1)

    query = (
        select(Schedule)
        .outerjoin(
            ScheduleDeactivation,
            Schedule.id == ScheduleDeactivation.schedule_id,
        )
        .where(
            or_(
                and_(
                    Schedule.active == True,
                    Schedule.is_fixed == True,
                    Schedule.user_id == user_id,
                ),
                and_(
                    ScheduleDeactivation.deactivation_date >= first_day,
                    ScheduleDeactivation.deactivation_date <= last_day,
                    ScheduleDeactivation.user_id == user_id,
                ),
            )
        )
    )

    results = session.scalars(query).all()

    return results


def clean_group_date(session: Session, user_id, scheduler: dict):
    filtered_dates = [
        date
        for date in scheduler["dates_generate"]
        if date >= scheduler["date_fixed"]
    ]

    date_canceled_result = (
        session.execute(
            select(ScheduleDeactivation.deactivation_date).where(
                and_(
                    ScheduleDeactivation.user_id == user_id,
                    ScheduleDeactivation.schedule_id == scheduler["id"],
                )
            )
        )
        .scalars()
        .first()
    )

    if date_canceled_result:
        if isinstance(date_canceled_result, date):
            date_canceled_result = datetime.combine(
                date_canceled_result, datetime.min.time()
            )

        filtered_dates = [
            date
            for date in filtered_dates
            if date <= date_canceled_result.date()
        ]

    return filtered_dates
