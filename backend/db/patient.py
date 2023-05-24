from db.base import Base, engine
from db.user import User
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Patient(User):
    __tablename__ = 'Patient'

    id = Column(Integer, ForeignKey('User.id'), primary_key=True, nullable=False, unique=True)
    status_id = Column(Integer, ForeignKey('Status.id'))

    status = relationship('Status')
    doctors = relationship('Doctor', secondary='Appointment')

