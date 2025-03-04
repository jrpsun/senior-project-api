from sqlalchemy import Column, String, Date, ForeignKey
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation

class ApplicantAddressThai(Base):
    __tablename__ = 'Applicant_Adress_Thai'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    houseNumber = Column(String(50), nullable=True)
    moo = Column(String(50), nullable=True)
    subDistrict = Column(String(50), nullable=True)
    district = Column(String(50), nullable=True)
    province = Column(String(50), nullable=True)
    postalCode = Column(String(50), nullable=True)
    village = Column(String(50), nullable=True)
    soi = Column(String(50), nullable=True)
    street = Column(String(50), nullable=True)