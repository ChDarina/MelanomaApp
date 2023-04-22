from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from base import Base, engine


class Doctor(Base):
    __tablename__ = 'Doctor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False, unique=True)
    specialty_id = Column(Integer, ForeignKey('Specialty.id'), nullable=False)
    education_id = Column(Integer, ForeignKey('Education.id'), nullable=False)
    work_years = Column(Integer, nullable=False)
    description = Column(String)

    user = relationship('User')
    specialty = relationship('Specialty')
    education = relationship('Education')
    workplaces = relationship('WorkPlace', secondary='DoctorJobs')
    appointments = relationship('Appointment', secondary='Appointment')

    __table_args__ = (UniqueConstraint('user_id', name='doctor_user_id_unique'),)


# create the table in the database
Base.metadata.create_all(engine)
