from db.base import Base, engine
from db.user import User
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship


class Doctor(User):
    __tablename__ = 'Doctor'

    id = Column(Integer, ForeignKey('User.id'), primary_key=True, nullable=False, unique=True)
    work_years = Column(Integer, nullable=False)
    description = Column(String(255))

    work_places = relationship('WorkPlace', secondary='DoctorJobs')
    patients = relationship('Patient', secondary='Appointment')


# create the table in the database
Base.metadata.create_all(engine)
