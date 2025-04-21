from sqlalchemy import Column, String, Text, ForeignKey, Integer
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantStatus(Base):
    __tablename__ = 'Applicant_Status'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    admissionStatus = Column(String(50), nullable=True)
    docStatus = Column(String(50), nullable=True)
    paymentStatus = Column(String(50), nullable=True)
    interviewStatus = Column(String(50), nullable=True)
    applyDate = Column(String(50), nullable=True)