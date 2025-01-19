from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from app.admin.schemas import UserProfileAdmin
from app.config.models import ProfessionalRecord, User
from fastapi import HTTPException

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
        cep=user.professional_record.cep
    )
    return user_profile
