from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from core.configs import settings

engine = create_engine(settings.DB_URL)

Session = sessionmaker(
    autocommit       = False,
    autoflush        = False,
    expire_on_commit = False,
    class_           = Session,
    bind             = engine
)
