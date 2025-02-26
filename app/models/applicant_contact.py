from sqlalchemy import Column, String, Date, ForeignKey, Text
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation

class ApplicantContact(Base):
    __tablename__ = 'Applicant_Contact'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    phoneNumber = Column(String(50))
    email = Column(String(50))
    line = Column(String(50))
    facebook = Column(String(50))
    instagram = Column(String(50))