from http import HTTPStatus

from fastapi import HTTPException


def check_admin(current_user):
    if not current_user.is_adm:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="You not have Authorization for this",
        )
