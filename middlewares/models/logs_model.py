from sqlalchemy import Column, Integer, String,  DATETIME

from core.configs import settings

class LogModel(settings.DBBaseModel):
    id          = Column(Integer, primary_key=True, autoincrement=True),
    full_log    = Column(String, nullable=False)
    log_level   = Column(String, nullable=False)
    issued_from = Column(String, nullable=False)
    issued_at   = Column(DATETIME, nullable=False)
    