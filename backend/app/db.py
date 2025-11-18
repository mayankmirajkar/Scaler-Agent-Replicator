from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

database_url = settings.database_url

# SQLite needs special connect_args
if database_url.startswith("sqlite"):
    engine = create_engine(
        database_url,
        future=True,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(database_url, future=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

Base = declarative_base()
