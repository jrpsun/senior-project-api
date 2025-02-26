from sqlalchemy import Column, String, Text, ForeignKey, Integer
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantAdditionalDocuments(Base):
    __tablename__ = 'Applicant_Additional_Documents'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    stateOfPurpose = Column(LONGTEXT)
    portfolio = Column(LONGTEXT)
    vdo = Column(String(255))
    resume = Column(LONGTEXT)
    additional = Column(LONGTEXT)