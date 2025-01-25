from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select, and_

from app.admin.schemas import UserProfileAdmin, ScheduledSchema
from app.config.models import ProfessionalRecord, Schedule, User


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


def get_scheduler_user(session: Session, user_id: id, offset: int, limit: int):
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
        and_(
            Schedule.active == True,
            Schedule.date_scheduled >= data_min
        )
    ) 
    if data_max:
        query = query.where(Schedule.date_scheduled <= data_max)

    result = session.scalars(
        query.offset(offset).limit(limit).order_by(Schedule.date_scheduled.desc())
    ).all()

    prox_index = 1 + limit if len(result) == limit else None
    result_data = [ScheduledSchema.from_orm(agendamento) for agendamento in result]
    return {
        "prox_index": prox_index,
        "scheduled": result_data
    }

def fechamento_mes_por_usuario_e_scheduler(
    session: Session,
    ano: int = datetime.now().year,  # Ano atual por padrão
    mes: int = datetime.now().month,  # Mês atual por padrão
):
    # Primeira e última data do mês
    primeiro_dia = datetime(ano, mes, 1)
    ultimo_dia = datetime(ano, mes, 1) + timedelta(days=32)
    ultimo_dia = datetime(ultimo_dia.year, ultimo_dia.month, 1) - timedelta(days=1)

    # Consulta para contar o número total de agendamentos, fixos e extras e o total arrecadado por usuário
    agendamentos_por_usuario = session.query(
        Schedule.user_id,
        User.first_name,
        User.last_name,
        func.count(Schedule.id).label("total_agendamentos"),
        func.sum(Schedule.price).label("total_value"),
        func.sum(Schedule.is_recurring).label("total_fixos"),
        func.sum(~Schedule.is_recurring).label("total_extras")
    ).join(User).filter(
        Schedule.date_scheduled >= primeiro_dia,
        Schedule.date_scheduled <= ultimo_dia
    ).group_by(Schedule.user_id, User.first_name, User.last_name).all()

    # Se houver agendamentos, formatamos o resultado
    if agendamentos_por_usuario:
        resultado = []
        for usuario in agendamentos_por_usuario:
            user_id, first_name, last_name, total_agendamentos, total_value, total_fixos, total_extras = usuario
            
            # Agora buscamos os agendamentos feitos por cada usuário no mês
            agendamentos_usuario = session.query(Schedule).filter(
                Schedule.user_id == user_id,
                Schedule.date_scheduled >= primeiro_dia,
                Schedule.date_scheduled <= ultimo_dia
            ).all()

            # Preparando a lista de agendamentos
            detalhes_agendamentos = [
                {
                    "id": agendamento.id,
                    "date_scheduled": agendamento.date_scheduled.isoformat(),
                    "time_scheduled": agendamento.time_scheduled,
                    "room": agendamento.room,
                    "type_scheduled": agendamento.type_scheduled,
                    "is_recurring": agendamento.is_recurring
                }
                for agendamento in agendamentos_usuario
            ]

            # Adicionando as informações do usuário e seus agendamentos
            resultado.append({
                "user_id": user_id,
                "name": f"{first_name} {last_name}",
                "total_agendamentos": total_agendamentos,
                "total_value": total_value,
                "total_fixos": total_fixos,
                "total_extras": total_extras,
                "agendamentos": detalhes_agendamentos
            })
        
        # Retornar a lista de usuários e seus agendamentos detalhados
        return {"mes": mes, "ano": ano, "usuarios": resultado}
    
    return {"message": "Nenhum agendamento encontrado para o mês solicitado."}