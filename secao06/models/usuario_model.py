from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from core.configs import settings
from typing import Any

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = "usuarios"
    id: Any = Column(Integer, primary_key=True, autoincrement=True)
    nome: Any = Column(String(256), nullable=True)
    sobrenome: Any = Column(String(256), nullable=True)
    email: Any = Column(String(256), index=True, unique=True, nullable=False)
    senha: Any = Column(String(256), nullable=False)
    eh_admin: Any = Column(Boolean, default=False)
    artigos = relationship("ArtigoModel", cascade="all, delete-orphan", back_populates="criador", uselist=True, lazy="joined")
