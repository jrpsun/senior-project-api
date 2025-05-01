from sqlalchemy import Column, String, ForeignKey
from app.db import Base
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations

class ApplicantAdmissionChannel(Base):
    __tablename__ = 'Applicant_Admission_Channel'

    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    onlineChannel = Column(String(50), nullable=True)
    offlineChannel = Column(String(50), nullable=True)
