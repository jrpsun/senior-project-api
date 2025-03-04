from sqlalchemy import Column, String, Date, ForeignKey
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation

class ApplicantContactPerson(Base):
    __tablename__ = 'Applicant_Contact_Person'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    thName = Column(String(50), nullable=True)
    enName = Column(String(50), nullable=True)
    relationship = Column(String(50), nullable=True)
    phoneNumber = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)