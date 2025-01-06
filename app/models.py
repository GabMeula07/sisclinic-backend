from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_adm = Column(Boolean, default=False)
    professional_record = relationship(
        "ProfessionalRecord", back_populates="user", uselist=False
    )
    schedule = relationship("Schedule", back_populates="user", uselist=False)


class ProfessionalRecord(Base):
    __tablename__ = "professional_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    birth = Column(Date, nullable=False)
    cpf = Column(String, nullable=False)
    occupation = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    number_record = Column(String, nullable=False)
    street = Column(String, nullable=False)
    number = Column(Integer)
    not_number = Column(Boolean, default=False)
    neighborhood = Column(String, nullable=False)
    city = Column(String, nullable=False)
    cep = Column(String, nullable=False)

    user = relationship("User", back_populates="professional_record")


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    date_scheduled = Column(Date, nullable=False)
    time_scheduled = Column(String, nullable=False)
    room = Column(String, nullable=False)
    type_scheduled = Column(String, nullable=False)
    active = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="schedule")


class ScheduleDeactivation(Base):
    __tablename__ = "schedule_deactivation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    deactivation_date = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relacionamentos
    schedule = relationship("Schedule")
    user = relationship("User")
