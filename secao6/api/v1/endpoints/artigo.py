from typing import List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.artigo_schema import ArtigoSchema

from models.__all__models import UsuarioModel, ArtigoModel

from core.deps import get_session, get_current_user

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(
    artigo: ArtigoSchema,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    novo_artigo = ArtigoModel(
        titulo=artigo.titulo,
        descricao=artigo.descricao,
        url_fonte=artigo.url_fonte,
        usuario_id=usuario_logado.id,
    )

    db.add(novo_artigo)
    await db.commit()

    return novo_artigo


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ArtigoSchema])
async def get_artigo(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()
        if len(artigos) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Nehnum artigo existente!"
            )
        return artigos


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ArtigoSchema)
async def get_artigo(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()

    if artigo == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado"
        )
    return artigo


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ArtigoSchema)
async def put_artigo(
    id: int,
    artigo: ArtigoSchema,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == id)
        result = await session.execute(query)
        artigo_up = result.scalars().unique().one_or_none()
    
        if artigo_up == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado"
            )
            
        if artigo_up.usuario_id != usuario_logado.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Somente o dono do artigo tem permissão para editá-lo"
            )
        artigo_up.titulo = artigo.titulo or artigo_up.titulo
        artigo_up.descricao = artigo.descricao or artigo_up.descricao
        artigo_up.url_fonte = artigo.url_fonte or artigo_up.url_fonte
        await session.commit()
        return artigo_up

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(
    id: int, 
    usuario_logado: UsuarioModel = Depends(get_current_user), 
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == id)
        result = await session.execute(query)
        artigo = result.scalars().unique().one_or_none()
    if artigo == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado!"
        )
    if artigo.usuario_id != usuario_logado.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Somente o dono do artigo tem permissão para exclui-lo"
        )
    await db.delete(artigo)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
