from sqlalchemy import Column, String
from app.db import Base


class ApplicantRegistrations(Base):
    __tablename__ = 'ApplicantRegistrations'

    applicantId = Column(String(50), primary_key=True)
    idCardNumber = Column(String(50), nullable=True)
    passportId = Column(String(50), nullable=True)
    applicantEmail = Column(String(50))
    prefix = Column(String(50))
    firstnameTH = Column(String(50), nullable=True, index=True)
    firstnameEN = Column(String(50), index=True)
    lastnameTH = Column(String(50), nullable=True, index=True)
    lastnameEN = Column(String(50), index=True)
    nationality = Column(String(50))
    password = Column(String(255))