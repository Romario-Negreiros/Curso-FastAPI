from typing import List, Optional, Any

from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import (
    UsuarioSchemaBase,
    UsuarioSchemaCreate,
    UsuarioSchemaUp,
    UsuariosSchemaArtigos,
)

from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()


@router.get("/logado", response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase
)
async def post_usuario(
    usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)
):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
    )
    async with db as session:
        session.add(novo_usuario)
        await session.commit()
        
        return novo_usuario
    
@router.get("/", status_code=status.HTTP_200_OK , response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
        
        return usuarios

@router.get("/{id}", response_model=UsuariosSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == id)
        result = await session.execute(query)
        usuario: UsuariosSchemaArtigos = result.scalars().unique().one_or_none()
    if usuario == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="O usuário não foi encontrado!")
    else:
        return usuario

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UsuarioSchemaBase)
async def put_usuario(id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        if usuario_up == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="O usuário não foi encontrado!")
        else:
            usuario_up.nome = usuario.nome or usuario_up.nome
            usuario_up.sobrenome = usuario.sobrenome or usuario_up.sobrenome
            usuario_up.email = usuario.email or usuario_up.email
            usuario_up.eh_admin = usuario.eh_admin or usuario_up.eh_admin
            usuario_up.senha = gerar_hash_senha(usuario.senha) if usuario.senha != None else usuario_up.senha
            
            await session.commit()
            return usuario_up
            
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        if usuario_del == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="O usuário não foi encontrado!")
        else:
            await session.delete(usuario_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, default="Dados de acesso incorretos.")
    
    return JSONResponse({"access_token": criar_token_acesso(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
