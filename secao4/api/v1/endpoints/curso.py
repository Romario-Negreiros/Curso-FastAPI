from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schema import CursoSchema
from core.deps import get_session

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CursoSchema)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
    db.add(novo_curso)
    await db.commit()
    
    return novo_curso

@router.get("/", response_model=List[CursoSchema])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    # try:
        cursos: List[CursoModel] = []
        async with db as session:
            query = select(CursoModel)
            result = await session.execute(query)
            cursos: List[CursoModel] = result.scalars().all()
            if len(cursos) == 0:
                return Response(status_code=status.HTTP_404_NOT_FOUND, content="Curso não encontrado.")
                
            return cursos
    # except:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        
@router.get("/{id}", response_model=CursoSchema, status_code=status.HTTP_200_OK)
async def get_curso(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()
        
        if curso:
            return curso
        else:
            raise HTTPException(detail='Curso não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

@router.put("/{id}", response_model=CursoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_curso(id: int, curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await session.execute(query)
        curso_up = result.scalar_one_or_none()
        if not curso_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')
        await session.delete(curso)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        