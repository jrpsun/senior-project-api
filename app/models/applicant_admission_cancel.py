from sqlalchemy import Column, String, Text, ForeignKey
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantAdmissionCancel(Base):
    __tablename__ = 'Applicant_Admission_Cancel'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    reason = Column(Text, nullable=True)
    moreDetail = Column(Text, nullable=True)