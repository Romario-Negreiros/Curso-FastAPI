from fastapi import APIRouter

from api.v1.endpoints import artigo
from api.v1.endpoints import usuarios

api_router = APIRouter()

api_router.include_router(artigo.router, prefix="/artigos", tags=["artigos"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
