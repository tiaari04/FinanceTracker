import os # used to be able to load my environment variables
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator 

load_dotenv()

_engine = None
SessionLocal = None
Base = declarative_base()

def init_engine():
    """Initialize the engine + session factory using env vars."""
    global _engine, SessionLocal
    if _engine is None:
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_pwd = os.getenv("DB_PWD")

        connection_string = f"postgresql+psycopg2://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"
        _engine = create_engine(connection_string)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def get_engine():
    if _engine is None:
        init_engine()
    return _engine

def get_db() -> Generator:
    if SessionLocal is None:
        init_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()