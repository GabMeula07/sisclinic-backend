from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=False)
    address = relationship("Address", back_populates="user", uselist=False)
    professional_record = relationship(
        "ProfessionalRecord", back_populates="user", uselist=False
    )


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    street = Column(String, nullable=False)
    number = Column(Integer)
    not_number = Column(Boolean, default=False)
    neighborhood = Column(String, nullable=False)
    city = Column(String, nullable=False)
    cep = Column(String, nullable=False)

    user = relationship("User", back_populates="address")


class ProfessionalRecord(Base):
    __tablename__ = "professional_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    birth = Column(Date, nullable=False)
    cpf = Column(String, nullable=False)
    occupation = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    number_record = Column(String, nullable=False)

    user = relationship("User", back_populates="professional_record")