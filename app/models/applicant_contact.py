from sqlalchemy import Column, String, Date, ForeignKey, Text
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation

class ApplicantContact(Base):
    __tablename__ = 'Applicant_Contact'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    aoolicantPhoneNumber = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    line = Column(String(50), nullable=True)
    facebook = Column(String(50), nullable=True)
    instagram = Column(String(50), nullable=True)