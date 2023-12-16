from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SyncSession
from sqlalchemy import create_engine

from core.configs import settings

engine = create_engine(settings.DB_URL)

Session: SyncSession = sessionmaker(
    autocommit       = False,
    autoflush        = False,
    expire_on_commit = False,
    class_           = SyncSession,
    bind             = engine
)
