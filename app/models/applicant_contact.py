from sqlalchemy import Column, String, ForeignKey
from app.db import Base
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations

class ApplicantContact(Base):
    __tablename__ = 'Applicant_Contact'

    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    applicantPhone = Column(String(50), nullable=True)
    #applicantEmail = Column(String(50), nullable=True)
    line = Column(String(50), nullable=True)
    facebook = Column(String(50), nullable=True)
    instagram = Column(String(50), nullable=True)