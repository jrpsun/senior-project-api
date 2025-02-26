from sqlalchemy import Column, String, Date, ForeignKey, Text
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation

class ApplicantAdressForeigner(Base):
    __tablename__ = 'Applicant_Adress_Foreigner'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    addr1 = Column(Text)
    addr2 = Column(Text)
    country = Column(String(50))
    city = Column(String(50))
    postalCode = Column(String(50))