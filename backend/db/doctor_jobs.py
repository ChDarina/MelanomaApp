from db.base import Base, engine
from sqlalchemy import Column, Integer, ForeignKey


class DoctorJobs(Base):
    __tablename__ = 'DoctorJobs'

    id = Column(Integer, autoincrement=True, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'))
    work_place_id = Column(Integer, ForeignKey('WorkPlace.id'))


# create the table in the database
Base.metadata.create_all(engine)
