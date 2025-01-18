from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.admin.services import check_admin

admin_routes = APIRouter(prefix="/admin", dependencies=[Depends(get_current_user)])


@admin_routes.get("/")
def hello_world(current_user = Depends(get_current_user)):
    check_admin(current_user)
    return {"msg": "Hello Admin"}

@admin_routes.get("/users/")
def get_all_users(
    current_user = Depends(get_current_user)
):
    check_admin(current_user)
    return {"msg": "Hello Admin"}