from sqlalchemy import Column, String, Date, ForeignKey, Text
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation

class ApplicantAdressForeigner(Base):
    __tablename__ = 'Applicant_Adress_Foreigner'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    addr1 = Column(Text, nullable=True)
    addr2 = Column(Text, nullable=True)
    country = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    postalCode = Column(String(50), nullable=True)