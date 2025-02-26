from sqlalchemy import Column, String, Date, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantAcademicBackgroundTypeB(Base):
    __tablename__ = 'Applicant_Academic_Background_TypeB'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    currentStatus = Column(String(50))
    graduateDate = Column(Date)
    mathematics = Column(Float)
    science = Column(Float)
    socialStudies = Column(Float)
    languageArts = Column(Float)
    docCopyTrans = Column(LONGTEXT)