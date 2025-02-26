from sqlalchemy import Column, String, Date, ForeignKey, Float, Text
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantAcademicBackgroundTypeD(Base):
    __tablename__ = 'Applicant_Academic_Background_TypeD'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    currentStatus = Column(String(50))
    graduateDate = Column(Date)
    country = Column(String(50))
    province = Column(String(50))
    schoolName = Column(String(50))
    studyPlan = Column(String(50))
    cumulativeGPA = Column(Float)
    comSciTitle = Column(Text)
    comSciCredit = Column(Float)
    docCopyTrans = Column(LONGTEXT)