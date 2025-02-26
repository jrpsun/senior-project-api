from sqlalchemy import Column, String, Date, ForeignKey
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation

class ApplicantAdmissionChannel(Base):
    __tablename__ = 'Applicant_Admission_Channel'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    onlineChannel = Column(String(50))
    offlineChannel = Column(String(50))
