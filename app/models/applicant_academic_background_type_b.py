from sqlalchemy import Column, String, Date, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantAcademicBackgroundTypeB(Base):
    __tablename__ = 'Applicant_Academic_Background_TypeB'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    currentStatus = Column(String(50), nullable=True)
    graduateDate = Column(String(50), nullable=True)
    mathematics = Column(Float, nullable=True)
    science = Column(Float, nullable=True)
    socialStudies = Column(Float, nullable=True)
    languageArts = Column(Float, nullable=True)
    docCopyTrans = Column(LONGTEXT, nullable=True)