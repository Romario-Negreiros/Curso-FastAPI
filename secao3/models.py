from typing import Optional

from pydantic import BaseModel, validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @validator("titulo")
    def validarTitulo(cls, value: str):
        palavras = value.split(" ")
        if len(palavras) > 3:
            raise ValueError("O título deve ter menos q 3 palavras")
        if value.islower():
            raise ValueError("O título deve estar capitalizado")

        return value
    
    @validator("aulas")
    def validarAulas(cls, value: int):
        if value < 10:
            raise ValueError("Aulas deve ser maior que 10")


cursos = [
    Curso(id=1, titulo="Progamação", aulas=112, horas=58),
    Curso(id=2, titulo="Algoritmos", aulas=12, horas=5),
    Curso(id=3, titulo="Dados", aulas=27, horas=15),
    Curso(id=4, titulo="Matematica", aulas=90, horas=54),
]
