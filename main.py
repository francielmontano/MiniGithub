from fastapi import FastAPI
from app.server.routers import  router_user
from app.server.configure import settings

app = FastAPI(
    title= settings.app_name,
    version= settings.app_version
)

app.include_router(router_user,prefix="/user")

@app.get("/")
async def healt():
    return "Bienvenido a tu API FastAPI"