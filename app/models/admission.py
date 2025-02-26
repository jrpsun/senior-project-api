from sqlalchemy import Column, String, Date
from app.db import Base


class Admission(Base):
    __tablename__ = 'Admission'

    admissionId = Column(String(50), primary_key=True)
    program = Column(String(255))
    roundName = Column(String(255))
    academicYear = Column(String(50))
    startDate = Column(Date)
    endDate = Column(Date)