from sqlalchemy import Column, String, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantDuolingo(Base):
    __tablename__ = 'Applicant_Duolingo'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    score = Column(Float, nullable=True)
    testDate = Column(String(50), nullable=True)
    literacy = Column(Float, nullable=True)
    comprehension = Column(Float, nullable=True)
    conversation = Column(Float, nullable=True)
    production = Column(Float, nullable=True)
    DuoCer = Column(LONGTEXT, nullable=True)