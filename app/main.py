import sys

sys.path.append("/home/gabrielmeula/projects/sisclinic_simplified")

from http import HTTPStatus

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.cruds import create_user
from app.database import get_session
from app.schemas import UserPublic, UserSchema

app = FastAPI()


# register endpoint
@app.post("/user/", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def post_user(user: UserSchema, db_session: Session = Depends(get_session)):
    db_user = create_user(session=db_session, user=user)
    return db_user
