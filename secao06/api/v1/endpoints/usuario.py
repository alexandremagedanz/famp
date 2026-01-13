from typing import List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaArtigos, UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp
from core.deps import get_section, get_current_user 
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()

@router.get('/logado', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK, summary="Retorna os dados do Usuário Logado", description="Essa rota retorna o usuário logado.", tags=["Usuários"])
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

@router.post('/singup', response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED, summary="Cria um novo usuário", description="Essa rota cria um novo usuário no banco de dados.", tags=["Usuários"])
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_section)):
    novo_usuario = UsuarioModel(nome=usuario.nome, sobrenome=usuario.sobrenome, email=usuario.email, senha=gerar_hash_senha(usuario.senha), eh_admin=usuario.eh_admin)
    async with db as session:
        session.add(novo_usuario)
        await session.commit()
        return novo_usuario
    
@router.get('/', response_model=List[UsuarioSchemaBase], status_code=status.HTTP_200_OK, summary="Retorna todos os usuários", description="Essa rota retorna todos os usuários cadastrados no banco de dados.", tags=["Usuários"])
async def get_usuarios(db: AsyncSession = Depends(get_section)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioModel] = result.scalars().unique().all()
        return usuarios

@router.get('/{usuario_id}', response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK, summary="Retorna um usuário", description="Essa rota retorna um usuário cadastrado no banco de dados.", tags=["Usuários"])
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_section)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
        if usuario:
            return usuario
        else:
            raise HTTPException(detail="Usuário nao encontrado", status_code=status.HTTP_404_NOT_FOUND)
        
@router.put('/{usuario_id}', response_model=UsuarioSchemaUp, status_code=status.HTTP_202_ACCEPTED, summary="Atualiza um usuário", description="Essa rota atualiza um usuário cadastrado no banco de dados.", tags=["Usuários"])
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_section)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.eh_admin:
                usuario_up.eh_admin = usuario.eh_admin
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)
            await session.commit()
            return usuario
        else:
            raise HTTPException(detail="Usuário nao encontrado", status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT, summary="Deleta um usuário", description="Essa rota deleta um usuário cadastrado no banco de dados.", tags=["Usuários"])
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_section)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Usuário nao encontrado", status_code=status.HTTP_404_NOT_FOUND)
        

@router.post('/login', summary="Faz login", description="Essa rota faz login no sistema.", tags=["Usuários"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_section)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos")
    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)