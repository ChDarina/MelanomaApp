from sqlalchemy import Column, Integer, String
from db.base import Base, engine


class Education(Base):
    __tablename__ = 'Education'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


# create the table in the database
Base.metadata.create_all(engine)
