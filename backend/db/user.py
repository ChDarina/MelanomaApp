from sqlalchemy import Column, Integer, String, ForeignKey, Date
from db.base import Base, engine
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey('Photo.id'), nullable=False)
    name = Column(String(255), nullable=False)
    birthday_date = Column(Date, nullable=False)
    residence = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    telephone = Column(String(15), nullable=False)
    password = Column(String(255), nullable=False)

    photo = relationship('Photo', uselist=False)


# create the table in the database
Base.metadata.create_all(engine)
