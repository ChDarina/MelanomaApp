from db.base import Base, engine
from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship


class DoctorsEducation(Base):
    __tablename__ = 'DoctorsEducation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'), nullable=False)
    education_id = Column(Integer, ForeignKey('Education.id'), nullable=False)
    education_specialty_id = Column(Integer, ForeignKey('EducationSpecialty.id'), nullable=False)
    graduation_date = Column(Date, nullable=False)

    doctors = relationship('Doctor', backref='DoctorsEducation', viewonly=True)
    educations = relationship('Education', viewonly=True)
    education_specialties = relationship('EducationSpecialty', viewonly=True)


# create the table in the database
Base.metadata.create_all(engine)
