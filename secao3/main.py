from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status

# from fastapi.responses import JSONResponse # tem bug
from fastapi import Response
from fastapi import Path  # adiociona validações extras para os parametros de url

# from fastapi import Query
from fastapi import Header
from fastapi import Depends

from time import sleep

from models import Curso
from models import cursos


def fakeDb():
    try:
        print("Abrindo conexão com banco de dados...")
        sleep(1)
    finally:
        print("Fechando conexão com banco de dados...")
        sleep(1)


app = FastAPI(
    title="API do curso", version="0.0.1", description="Api para estudo do fast api"
)

@app.get(
    "/cursos",
    description="Retorna todos cursos ou uma lista vazia",
    summary="Retorna todos os cursos",
    response_model=List[Curso],
    response_description="Cursos encontrados com sucesso"
)
async def getCursos(db: Any = Depends(fakeDb)):
    return cursos


@app.get("/cursos/{id}", status_code=status.HTTP_200_OK)  # greater than / lower than
async def getCurso(
    id: int = Path(title="Id do curso", description="Range(1,2)", gt=0, lt=3)
):
    curso = next((curso for curso in cursos if curso.id == id), False) # next iterator
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado."
        )
    return curso


@app.post("/cursos", status_code=status.HTTP_201_CREATED, response_model=Curso)
async def postCurso(curso: Curso):
    nextId: int = len(cursos) + 1
    curso.id = nextId
    cursos.append(curso)
    return curso


@app.put("/cursos/{id}", status_code=status.HTTP_200_OK)
async def putCurso(id: int, curso: Curso):
    if id not in cursos:
        raise HTTPException(
            status_code=status.HTTP_404_CONFLICT, detail="O curso não existe!"
        )
    cursos[id] = curso
    del curso.id
    return curso


@app.delete("/cursos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteCurso(id: int):
    if id not in cursos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="O curso não existe!"
        )
    cursos.pop(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Exemplo de uso das query strings
# @app.get("/calculadora")
# async def calculadora(a: int = Query(title="a", description="Valor de a"), b: int = Query(gt=2), c: int = 0):
#     return f"Resultado: {a + b + c}"


# Exemplo headers
@app.get("/test_header")
async def calculadora(x_header: str = Header()):
    return f"Header recebido: {x_header}"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
