import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv(f".env")

engine = create_engine(os.getenv('ENGINE_URL'))

Session = sessionmaker(bind=engine)

Base = declarative_base()
Base.metadata.bind = engine


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
