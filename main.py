from fastapi import FastAPI
from app.server.routers import  router_user

app = FastAPI()

app.include_router(router_user,prefix="/user")

@app.get("/")
async def healt():
    return "Bienvenido a tu API FastAPI"