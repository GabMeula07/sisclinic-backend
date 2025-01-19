from datetime import date
from typing import List

from pydantic import BaseModel


class UserAdmin(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    is_active: bool


class AllUserAdmin(BaseModel):
    users_list: List[UserAdmin]


class UserProfileAdmin(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    birth: date
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
