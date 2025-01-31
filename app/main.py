from fastapi import FastAPI

from app.admin.routes import admin_routes
from app.users.routes import user_routes

app = FastAPI()
app.include_router(admin_routes, tags=["Admin"])
app.include_router(user_routes)
