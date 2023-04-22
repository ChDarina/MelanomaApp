from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from base import Base, engine


class Appointment(Base):
    __tablename__ = 'Appointment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    patients = relationship('Patient', back_populates='appointments')
    doctors = relationship('Doctor', back_populates='appointments')


# create the tables in the database
Base.metadata.create_all(engine)
