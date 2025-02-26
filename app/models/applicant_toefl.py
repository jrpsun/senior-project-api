from sqlalchemy import Column, String, Date, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantTOEFL(Base):
    __tablename__ = 'Applicant_TOEFL'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    toeflType = Column(String(50))
    score = Column(Float)
    testDate = Column(Date)
    listening = Column(Float)
    reading = Column(Float)
    strucAndWrite = Column(Float)
    TOEFLCer = Column(LONGTEXT)