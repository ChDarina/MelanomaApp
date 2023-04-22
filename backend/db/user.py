from sqlalchemy import Column, Integer, String
from base import Base, engine


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)


# create the table in the database
Base.metadata.create_all(engine)
