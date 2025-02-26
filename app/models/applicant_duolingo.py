from sqlalchemy import Column, String, Date, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantDuolingo(Base):
    __tablename__ = 'Applicant_Duolingo'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    score = Column(Float)
    testDate = Column(Date)
    literacy = Column(Float)
    comprehension = Column(Float)
    conversation = Column(Float)
    production = Column(Float)
    DuoCer = Column(LONGTEXT)