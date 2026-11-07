from fastapi import FastAPI
from app.server.routers import  router_user, router_repo

app = FastAPI()

app.include_router(router_user,prefix="/user")
app.include_router(router_repo,prefix="/repo")

@app.get("/")
async def healt():
    return "Bienvenido a tu API FastAPI"