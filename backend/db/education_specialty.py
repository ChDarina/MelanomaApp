from sqlalchemy import Column, Integer, String
from db.base import Base, engine


class EducationSpecialty(Base):
    __tablename__ = 'EducationSpecialty'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


# create the table in the database
Base.metadata.create_all(engine)
