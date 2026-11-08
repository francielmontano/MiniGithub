from fastapi import FastAPI
from app.server.routers import  router_user, router_repo, router_collab
from app.server.routers import  router_user, router_repo, router_auth
from app.server.configure import settings

app = FastAPI(
    title= settings.app_name,
    version= settings.app_version
)

app.include_router(router_user,prefix="/user")
app.include_router(router_repo,prefix="/repo")
app.include_router(router_collab,prefix="/collab")
app.include_router(router_auth, prefix="/auth")
@app.get("/")
async def healt():
    return "Bienvenido a tu API FastAPI"