from fastapi import Integer, String, Column

from core.configs import settings

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = "usuarios"
    
    cpf = Column(Integer)
    nome = Column(String)
