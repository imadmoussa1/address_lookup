from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(expire_on_commit=False, autocommit=False, autoflush=False, bind=engine)

def get_pg_db():
  db = SessionLocal()
  try:
    return db
  finally:
    db.close()
