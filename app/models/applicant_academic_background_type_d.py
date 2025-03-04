from sqlalchemy import Column, String, ForeignKey, Float, Text
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantAcademicBackgroundTypeD(Base):
    __tablename__ = 'Applicant_Academic_Background_TypeD'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    currentStatus = Column(String(50), nullable=True)
    graduateDate = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    province = Column(String(50), nullable=True)
    schoolName = Column(String(50), nullable=True)
    studyPlan = Column(String(50), nullable=True)
    cumulativeGPA = Column(Float, nullable=True)
    comSciTitle = Column(Text, nullable=True)
    comSciCredit = Column(Float, nullable=True)
    docCopyTrans = Column(LONGTEXT, nullable=True)