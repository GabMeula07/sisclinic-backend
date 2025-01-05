from datetime import date, datetime
from typing import List

from pydantic import BaseModel, EmailStr, PastDate, field_validator


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class ProfileSchema(BaseModel):
    birth: PastDate
    cpf: str
    occupation: str
    specialization: str
    number_record: str
    street: str
    number: int
    not_number: bool
    neighborhood: str
    city: str
    cep: str


class UserPublic(BaseModel):
    id: int
    email: str


class UserListSchema(BaseModel):
    users: list[UserPublic]


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


# Requisição para redefinir senha
class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class SchedulerRequestSchema(BaseModel):
    room: str
    date_scheduled: date
    time_scheduled: str
    type_scheduled: str

    @field_validator("date_scheduled", mode="before")
    def validate_date(cls, value):
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d").date()

        if value < date.today():  # Verifica se é anterior ao dia atual
            raise ValueError("A data deve ser hoje ou no futuro.")
        return value


class SchedulerListSchema(BaseModel):
    scheduled: List[SchedulerRequestSchema]
    msg: str


class ScheduledSchema(BaseModel):
    id: int
    user_id: int
    room: str
    date_scheduled: date
    time_scheduled: str
    type_scheduled: str


class ScheduledAdminListSchema(BaseModel):
    prox_index: int | None = None
    max_index: int | None = None
    scheduled: list[ScheduledSchema]
