import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.question import Base


class Database:
    def __init__(self):
        self.engine = create_engine(os.environ.get('DATABASE_URL'))
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.create_tables()

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def close(self):
        self.engine.dispose()


def get_db():
    db = Database().SessionLocal()
    try:
        yield db
    finally:
        db.close()


database = Database()
