import sys

sys.path.append("/home/gabrielmeula/projects/sisclinic_simplified")

from http import HTTPStatus

from fastapi import Depends, FastAPI, Form, HTTPException, status
from sqlalchemy.orm import Session

from app.cruds import create_user, get_user_by_email, update_user
from app.database import get_session  
from app.schemas import TokenSchema, UserPublic, UserSchema, PasswordResetRequest, PasswordResetConfirm
from app.security import create_access_token, get_current_user, verify_password, create_reset_token, verify_reset_token
from app.services import send_reset_email

app = FastAPI()


# register endpoint
@app.post("/user/", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def post_user(user: UserSchema, db_session: Session = Depends(get_session)):
    db_user = create_user(session=db_session, user=user)
    return db_user


@app.post("/token", response_model=TokenSchema)
async def login_user(
    username: str = Form(...),
    password: str = Form(...),
    db_session: Session = Depends(get_session),
):
    user = get_user_by_email(session=db_session, email=username)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid Email or Password",
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid Email or Password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

@app.post("/password-reset-request")
def password_reset_request(
    request: PasswordResetRequest,
    db_session: Session = Depends(get_session)
):

    user = get_user_by_email(session=db_session, email=request.email)
    token = create_reset_token({"sub": user.email})
    send_reset_email(user.email, token)

    return {"message": "Token enviado para o e-mail informado"}

@app.post("/password-reset")
def password_reset(
    request: PasswordResetConfirm,
    db_session: Session = Depends(get_session)
):
    # Verificar token
    email = verify_reset_token(request.token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado"
        )

    # Atualizar senha no banco
    user =  get_user_by_email(session=db_session, email=email)
    update_user(session=db_session, user=user, data = {'password': request.new_password} )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")


    return {"message": "Senha atualizada com sucesso"}