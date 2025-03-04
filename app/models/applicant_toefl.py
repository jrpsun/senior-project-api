from sqlalchemy import Column, String, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantTOEFL(Base):
    __tablename__ = 'Applicant_TOEFL'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    toeflType = Column(String(50), nullable=True)
    score = Column(Float, nullable=True)
    testDate = Column(String(50), nullable=True)
    listening = Column(Float, nullable=True)
    reading = Column(Float, nullable=True)
    strucAndWrite = Column(Float, nullable=True)
    TOEFLCer = Column(LONGTEXT, nullable=True)