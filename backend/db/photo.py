from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from db.base import Base, engine


class Photo(Base):
    __tablename__ = 'Photo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(255), nullable=False)

    __table_args__ = (UniqueConstraint('id', name='photo_id_unique'),)

