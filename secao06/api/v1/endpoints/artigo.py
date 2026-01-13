from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema
from core.deps import get_section, get_current_user 

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Cria um artigo", description="Essa rota cria um novo artigo no banco de dados.", response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema, usuario_logaado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_section)):
    novo_artigo = ArtigoModel(titulo=artigo.titulo, descricao=artigo.descricao, url_fonte=artigo.url_fonte, usuario_id=usuario_logaado.id)
    db.add(novo_artigo)
    await db.commit()
    return novo_artigo

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ArtigoSchema], summary="Retorna todos os artigos", description="Essa rota retorna todos os artigos cadastrados no banco de dados.")
async def get_artigos(db: AsyncSession = Depends(get_section)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = list(result.scalars().unique().all())
        return artigos 

@router.get("/{artigo_id}", status_code=status.HTTP_200_OK, response_model=ArtigoSchema, summary="Retorna um artigo", description="Essa rota retorna um artigos cadastrado no banco de dados.")
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_section)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()
        if artigo:
            return artigo
        else:
            raise HTTPException(detail="Artigo nao encontrado", status_code=status.HTTP_404_NOT_FOUND)

@router.put("/{artigo_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ArtigoSchema, summary="Atualiza um artigo", description="Essa rota atualiza um artigo cadastrado no banco de dados.")
async def put_artigo(artigo_id: int, artigo: ArtigoSchema, db: AsyncSession = Depends(get_section), usuario_logaado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_up: ArtigoModel = result.scalars().unique().one_or_none()
        if artigo_up:
            if artigo.titulo:
                artigo_up.titulo = artigo.titulo
            if artigo.descricao:
                artigo_up.descricao = artigo.descricao
            if artigo.url_fonte:
                artigo_up.url_fonte = artigo.url_fonte
            if usuario_logaado.id!= artigo_up.usuario_id:
                artigo_up.usuario_id = usuario_logaado.id
            await session.commit()
            return artigo_up
        else:
            raise HTTPException(detail="Artigo nao encontrado", status_code=status.HTTP_404_NOT_FOUND)
            
@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT,  summary="Deleta um artigo", description="Essa rota deleta um artigo cadastrado no banco de dados.")
async def delete_artigo(artigo_id: int, db: AsyncSession = Depends(get_section), usuario_logaado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id).filter(ArtigoModel.usuario_id == usuario_logaado.id)
        result = await session.execute(query)
        artigo_del: ArtigoModel = result.scalars().unique().one_or_none()
        if artigo_del:
            await session.delete(artigo_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Artigo nao encontrado", status_code=status.HTTP_404_NOT_FOUND)
            