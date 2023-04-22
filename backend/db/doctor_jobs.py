from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from base import Base, engine


class DoctorJobs(Base):
    __tablename__ = 'doctorJobs'

    doctor_id = Column(Integer, ForeignKey('Doctor.id'), primary_key=True)
    work_place_id = Column(Integer, ForeignKey('WorkPlace.id'), primary_key=True)

    doctor = relationship('Doctor', back_populates='jobs')
    workplace = relationship('WorkPlace', back_populates='jobs')


# create the table in the database
Base.metadata.create_all(engine)
