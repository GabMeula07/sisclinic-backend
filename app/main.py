from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.admin.routes import admin_routes
from app.users.routes import user_routes

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(admin_routes, tags=["Admin"])
app.include_router(user_routes)
