from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint
from base import Base, engine


class Patient(Base):
    __tablename__ = 'Patient'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    status_id = Column(Integer, ForeignKey('Status.id'))

    user = relationship('User')
    status = relationship('Status')
    appointments = relationship('Appointment', secondary='Appointment')

    __table_args__ = (UniqueConstraint('user_id', name='patient_user_id_unique'),)


# create the table in the database
Base.metadata.create_all(engine)
