from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base, engine


class WorkPlace(Base):
    __tablename__ = 'WorkPlace'

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('Company.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    description = Column(String(255))

    company = relationship('Company')
    doctors = relationship('Doctor')


# create the table in the database
Base.metadata.create_all(engine)
