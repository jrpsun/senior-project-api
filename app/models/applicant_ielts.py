from sqlalchemy import Column, String, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantIELTS(Base):
    __tablename__ = 'Applicant_IELTS'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    score = Column(Float, nullable=True)
    testDate = Column(String(50), nullable=True)
    listening = Column(Float, nullable=True)
    speaking = Column(Float, nullable=True)
    reading = Column(Float, nullable=True)
    writing = Column(Float, nullable=True)
    IELTSCer = Column(LONGTEXT, nullable=True)
