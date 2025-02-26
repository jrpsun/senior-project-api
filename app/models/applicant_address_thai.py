from sqlalchemy import Column, String, Date, ForeignKey
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation

class ApplicantAddressThai(Base):
    __tablename__ = 'Applicant_Adress_Thai'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    houseNumber = Column(String(50))
    moo = Column(String(50))
    subDistrict = Column(String(50))
    district = Column(String(50))
    province = Column(String(50))
    postalCode = Column(String(50))
    village = Column(String(50))
    soi = Column(String(50))
    street = Column(String(50))