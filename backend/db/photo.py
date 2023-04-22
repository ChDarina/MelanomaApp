from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from base import Base, engine


class Photo(Base):
    __tablename__ = 'Photo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(255), nullable=False)
    predict_session = relationship('PredictSession', uselist=False, back_populates='photo')

    __table_args__ = (UniqueConstraint('id', name='photo_id_unique'),)


# create the table in the database
Base.metadata.create_all(engine)
