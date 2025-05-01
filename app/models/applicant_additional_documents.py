from sqlalchemy import Column, String, ForeignKey
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations


class ApplicantAdditionalDocuments(Base):
    __tablename__ = 'Applicant_Additional_Documents'

    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    stateOfPurpose = Column(LONGTEXT, nullable=True)
    stateOfPurposeName = Column(String(255), nullable=True)
    stateOfPurposeSize = Column(String(50), nullable=True)
    portfolio = Column(LONGTEXT, nullable=True)
    portfolioName = Column(String(255), nullable=True)
    portfolioSize = Column(String(255), nullable=True)
    vdo = Column(String(255), nullable=True)
    applicantResume = Column(LONGTEXT, nullable=True)
    applicantResumeName = Column(String(255), nullable=True)
    applicantResumeSize = Column(String(50), nullable=True)
    additional = Column(LONGTEXT, nullable=True)
    additionalName = Column(String(255), nullable=True)
    additionalSize = Column(String(50), nullable=True)