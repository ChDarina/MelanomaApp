from sqlalchemy import Column, Integer, String

from db.base import Base


class Company(Base):
    __tablename__ = 'Company'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
