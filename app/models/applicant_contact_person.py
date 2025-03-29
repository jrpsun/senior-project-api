from sqlalchemy import Column, String, Date, ForeignKey
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation

class ApplicantContactPerson(Base):
    __tablename__ = 'Applicant_Contact_Person'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    contactFirstNameTH = Column(String(50), nullable=True)
    contactMiddleNameTH = Column(String(50), nullable=True)
    contactLastNameTH = Column(String(50), nullable=True)
    contactFirstNameEN = Column(String(50), nullable=True)
    contactMiddleNameEN = Column(String(50), nullable=True)
    contactLastNameEN = Column(String(50), nullable=True)
    relationship = Column(String(50), nullable=True)
    contactPhone = Column(String(50), nullable=True)
    contactEmail = Column(String(50), nullable=True)