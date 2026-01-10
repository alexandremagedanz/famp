from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.curso_model import  CursoModel
from core.deps import get_session

#Bypass warning sqlmodel
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True
#Fim Bypass

router = APIRouter()
@router.post("/", response_model=CursoModel, status_code=status.HTTP_201_CREATED, summary="Cria um novo curso", description="Essa rota cria um novo curso no banco de dados.")
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
    db.add(novo_curso)
    await db.commit()
    return novo_curso

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CursoModel], summary="Lista todos os cursos", description="Essa rota lista todos os cursos cadastrados no banco de dados.")
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
        return cursos

@router.get("/{curso_id}", status_code=status.HTTP_200_OK, response_model=CursoModel, summary="Lista um curso específico", description="Essa rota lista um curso específico cadastrado no banco de dados.")
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()
        if curso:
            return curso
        else:
            raise HTTPException(detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)

@router.put("/{curso_id}", status_code=status.HTTP_202_ACCEPTED, response_model=CursoModel, summary="Atualiza um curso", description="Essa rota atualiza os dados de um curso específico no banco de dados.")
async def put_curso(curso_id: int, curso: CursoModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_up = result.scalar_one_or_none()
        if curso_up:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas

            await session.commit()
            return curso_up
        else:
            raise HTTPException(detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)
        
@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Deleta um curso", description="Essa rota deleta um curso específico do banco de dados.")
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_del = result.scalar_one_or_none()
        if curso_del:
            await session.delete(curso_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND) 