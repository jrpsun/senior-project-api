from sqlalchemy import Column, String, Date, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantTOEFLInternet(Base):
    __tablename__ = 'Applicant_TOEFL_Internet'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    score = Column(Float)
    testDate = Column(Date)
    listening = Column(Float)
    speaking = Column(Float)
    reading = Column(Float)
    writing = Column(Float)
    TOEFLInternetCer = Column(LONGTEXT)