from sqlalchemy import Column, String, ForeignKey
from app.db import Base
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations


class ApplicantStatus(Base):
    __tablename__ = 'Applicant_Status'

    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    admissionStatus = Column(String(50), nullable=True)
    docStatus = Column(String(50), nullable=True)
    paymentStatus = Column(String(50), nullable=True)
    interviewStatus = Column(String(50), nullable=True)
    applyDate = Column(String(50), nullable=True)