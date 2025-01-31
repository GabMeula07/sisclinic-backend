from datetime import date, datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_, func, or_, select

from app.admin.schemas import ScheduledSchema, UserProfileAdmin
from app.config.models import (
    ProfessionalRecord,
    Schedule,
    ScheduleDeactivation,
    User,
)

FIXED_COST = 25


def get_all_user(session: Session):
    result = session.query(User).all()
    return list(result)


def get_all_user_data(session: Session, user_id):
    user = (
        session.query(User)
        .join(ProfessionalRecord, User.id == ProfessionalRecord.user_id)
        .filter(User.id == user_id)
        .first()  # Usando .first() já que é possível que o usuário tenha apenas um perfil
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Supondo que você tenha os dados de ProfessionalRecord associados
    user_profile = UserProfileAdmin(
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        birth=user.professional_record.birth,
        cpf=user.professional_record.cpf,
        occupation=user.professional_record.occupation,
        specialization=user.professional_record.specialization,
        number_record=user.professional_record.number_record,
        street=user.professional_record.street,
        number=user.professional_record.number,
        not_number=user.professional_record.not_number,
        neighborhood=user.professional_record.neighborhood,
        city=user.professional_record.city,
        cep=user.professional_record.cep,
    )
    return user_profile


def get_scheduler_user(
    session: Session, user_id: int, offset: int, limit: int
):
    scheduler_list = (
        session.execute(
            select(Schedule)
            .where(Schedule.user_id == user_id)
            .order_by(Schedule.date_scheduled.desc(), Schedule.time_scheduled)
            .offset(offset)
            .limit(limit)
        )
        .scalars()
        .all()
    )  # Usamos .all() para pegar todos os resultados como uma lista

    # Verifica se há agendamentos e trata o caso de lista vazia
    if not scheduler_list:
        return {"prox_index": None, "max_index": None, "scheduled": []}

    # Converte os agendamentos em um formato mais amigável (como dicionário)
    result = [
        {
            "id": agendamento.id,
            "user_id": agendamento.user_id,
            "room": agendamento.room,
            "date_scheduled": agendamento.date_scheduled.isoformat()
            if isinstance(agendamento.date_scheduled, datetime)
            else agendamento.date_scheduled,
            "time_scheduled": agendamento.time_scheduled.isoformat()
            if isinstance(agendamento.time_scheduled, datetime)
            else agendamento.time_scheduled,
            "type_scheduled": agendamento.type_scheduled,
        }
        for agendamento in scheduler_list
    ]

    prox_index = offset + limit if len(scheduler_list) == limit else None

    # Retorna o resultado em formato JSON (list of dicts)
    return {
        "prox_index": prox_index,
        "scheduled": result,
    }


def get_all_schedulers(
    session: Session, offset: int, limit: int, data_min, data_max
):
    query = select(Schedule).where(
        and_(Schedule.active == True, Schedule.date_scheduled >= data_min)
    )
    if data_max:
        query = query.where(Schedule.date_scheduled <= data_max)

    result = session.scalars(
        query.offset(offset)
        .limit(limit)
        .order_by(Schedule.date_scheduled.desc())
    ).all()

    prox_index = 1 + limit if len(result) == limit else None
    result_data = [
        ScheduledSchema.from_orm(agendamento) for agendamento in result
    ]
    return {"prox_index": prox_index, "scheduled": result_data}


def clising_month_by_extra(
    session: Session,
    user_id: int,
    month,
    year,
):
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, 1) + timedelta(days=32)
    last_day = datetime(last_day.year, last_day.month, 1) - timedelta(days=1)

    scheduler_list = session.scalars(
        select(Schedule)
        .where(
            and_(
                Schedule.user_id == user_id,
                Schedule.date_scheduled >= first_day,
                Schedule.date_scheduled <= last_day,
                Schedule.is_fixed == False,
            )
        )
        .order_by(Schedule.date_scheduled)
    ).all()

    count = session.scalar(
        select(func.count(Schedule.id)).where(
            and_(
                Schedule.user_id == user_id,
                Schedule.date_scheduled >= first_day,
                Schedule.date_scheduled <= last_day,
                Schedule.is_fixed == False,
            )
        )
    )

    data = {
        "Quantidade de extra": count,
        "Total valor extra": count * FIXED_COST,
        "Schedulers": scheduler_list,
    }

    return data


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


def closing_date(session: Session, month: int, year: int): ...
