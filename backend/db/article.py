from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base import Base, engine


class Article(Base):
    __tablename__ = 'Article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(6000), nullable=False)
    datetime_created = Column(DateTime, nullable=False)

    doctor = relationship('Doctor')

