import sys
sys.path.append('/home/gabrielmeula/projects/sisclinic')

from fastapi import FastAPI
from sisclinic.api.v1.routes.user_routes import user_routes
app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello world!"}

app.include_router(user_routes)