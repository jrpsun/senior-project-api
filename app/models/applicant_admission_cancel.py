from sqlalchemy import Column, String, Text, ForeignKey
from app.db import Base
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations


class ApplicantAdmissionCancel(Base):
    __tablename__ = 'Applicant_Admission_Cancel'

    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    reason = Column(Text, nullable=True)
    moreDetail = Column(Text, nullable=True)