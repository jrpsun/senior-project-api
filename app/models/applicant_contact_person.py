from sqlalchemy import Column, String, ForeignKey
from app.db import Base
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations

class ApplicantContactPerson(Base):
    __tablename__ = 'Applicant_Contact_Person'

    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    contactFirstNameTH = Column(String(50), nullable=True)
    contactMiddleNameTH = Column(String(50), nullable=True)
    contactLastNameTH = Column(String(50), nullable=True)
    contactFirstNameEN = Column(String(50), nullable=True)
    contactMiddleNameEN = Column(String(50), nullable=True)
    contactLastNameEN = Column(String(50), nullable=True)
    relationship = Column(String(50), nullable=True)
    contactPhone = Column(String(50), nullable=True)
    contactEmail = Column(String(50), nullable=True)