from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


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