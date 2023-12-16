from sqlalchemy import String, Column, DATETIME

from core.configs import settings

class DocModel(settings.DBBaseModel):
    type: Column(String(256))
    owner: Column(String(256))
    emissionDate: Column(DATETIME)
