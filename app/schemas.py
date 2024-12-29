from pydantic import BaseModel, EmailStr, PastDate


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
