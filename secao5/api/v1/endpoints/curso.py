from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.curso_model import CursoModel
from core.deps import get_session

# Bypass warning SQLmodel select
# from sqlmodel.sql.expression import Select, SelectOfScalar

# SelectOfScalar.inherit_cache = True # type: ignore
# Select.inherit_cache = True # type: ignore
# Bypass end

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
    
    db.add(novo_curso)
    await db.commit()
    
    return novo_curso

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CursoModel])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    cursos: List[CursoModel] = []
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos = result.scalars().all()
        if len(cursos) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nnehum curso existente!")
        return cursos
    
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CursoModel)
async def get_curso(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()
        if not curso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado!")
        return curso

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=CursoModel)
async def put_curso(id: int, curso: CursoModel, db: AsyncSession = Depends(get_session)):
    if id != curso.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Os IDs não coincidem.")
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await session.execute(query)
        curso_up = result.scalar_one_or_none()
        if not curso_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado.") 
        curso_up.titulo = curso.titulo
        curso_up.aulas = curso.aulas
        curso_up.horas = curso.horas
        await session.commit()
        return curso_up
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()
        if not curso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado.") 
        await session.delete(curso)
        await session.commit() 
        return Response(status_code=status.HTTP_204_NO_CONTENT)
