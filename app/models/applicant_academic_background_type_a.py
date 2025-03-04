from sqlalchemy import Column, String, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicanntAcademicBackgroundTypeA(Base):
    __tablename__ = 'Applicant_Academic_Background_TypeA'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    currentStatus = Column(String(50), nullable=True)
    graduateDate = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    province = Column(String(50), nullable=True)
    schoolName = Column(String(100), nullable=True)
    studyPlan = Column(String(100), nullable=True)
    cumulativeGPA = Column(Float, nullable=True)
    english = Column(Float, nullable=True)
    mathematics = Column(Float, nullable=True)
    scitech = Column(Float, nullable=True)
    docCopyTrans = Column(LONGTEXT, nullable=True)