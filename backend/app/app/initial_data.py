import logging

from app.db.init_db import init_db
from app.db.session import SessionLocal, engine

from app.db.base import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
  Base.metadata.create_all(bind=engine)
  db = SessionLocal()
  init_db(db)


def main() -> None:
  logger.info("Creating initial data")
  init()
  logger.info("Initial data created")


if __name__ == "__main__":
  main()
