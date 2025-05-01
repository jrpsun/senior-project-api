from sqlalchemy import Column, String, ForeignKey
from app.db import Base
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations

class ApplicantAddress(Base):
    __tablename__ = 'Applicant_Adress'

    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    houseNumber = Column(String(50), nullable=True)
    moo = Column(String(50), nullable=True)
    subDistrict = Column(String(50), nullable=True)
    district = Column(String(50), nullable=True)
    province = Column(String(50), nullable=True)
    postalCode = Column(String(50), nullable=True)
    village = Column(String(50), nullable=True)
    soi = Column(String(50), nullable=True)
    street = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    addr1 = Column(String(255), nullable=True)
    addr2 = Column(String(255), nullable=True)
    city = Column(String(50), nullable=True)