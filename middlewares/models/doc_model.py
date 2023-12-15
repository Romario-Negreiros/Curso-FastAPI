from fastapi import Integer, String, Column

from core.configs import settings

class DocModel(settings.DBBaseModel):
    conteudo: Column(String(256))
