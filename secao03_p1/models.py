from typing import Optional
from pydantic import BaseModel, validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int #mais de 12
    horas: int #mais de 10

@validator('titulo')
def validar_titulo(cls, value):
    palavras = len(value.split(' '))
    #validação 1
    if palavras < 3:
        raise ValueError('O título deve conter ao menos tres palavras')
    #validação 2
    if value.lower():
        raise ValueError('O título deve ser capitalizado')
    return value

@validator('aulas')
def validar_aulas(cls, value):
    if value < 12:
        raise ValueError('O curso deve ter ao menos 12 aulas')
    return value

@validator('horas')
def validar_horas(cls, value):
    if value < 10:
        raise ValueError('O curso deve ter ao menos 10 horas')
    return value

cursos = [
    Curso(id=1, titulo="Programação para Leigos", aulas=112, horas=58),
    Curso(id=2, titulo="Algoritmos e Lógica de Programação", aulas=87, horas=67),
]