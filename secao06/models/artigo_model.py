from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings
from typing import Any

class ArtigoModel(settings.DBBaseModel):
    __tablename__ = "artigos"
    id: Any = Column(Integer, primary_key=True, autoincrement=True)
    titulo: Any= Column(String(256))
    descricao: Any = Column(String(256))
    url_fonte: Any = Column(String(256))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    criador = relationship("UsuarioModel", back_populates="artigos", lazy="joined")