from sqlalchemy import Column, String, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantAcademicBackground(Base):
    __tablename__ = 'Applicant_Academic_Background'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    academicType = Column(String(50), nullable=True)
    customAcademicType = Column(String(50), nullable=True)
    currentStatus = Column(String(50), nullable=True)
    graduateDate = Column(String(50), nullable=True)
    graduateYear = Column(String(50), nullable=True)
    academicCountry = Column(String(50), nullable=True)
    academicProvince = Column(String(50), nullable=True)
    schoolName = Column(String(100), nullable=True)
    studyPlan = Column(String(100), nullable=True)
    customStudyPlan = Column(String(100), nullable=True)
    cumulativeGPA = Column(String(50), nullable=True)
    dstEnglish = Column(String(50), nullable=True)
    dstMathematics = Column(String(50), nullable=True)
    dstScitech = Column(String(50), nullable=True)
    comSciTitle = Column(String(50), nullable=True)
    comSciCredit = Column(String(50), nullable=True)
    gedMathematics = Column(String(50), nullable=True)
    gedScience = Column(String(50), nullable=True)
    gedSocialStudies = Column(String(50), nullable=True)
    gedLanguageArts = Column(String(50), nullable=True)
    g12MathCredit = Column(String(50), nullable=True)
    g12MathTitle = Column(String(50), nullable=True)
    g12SciCredit = Column(String(50), nullable=True)
    g12SciTitle = Column(String(50), nullable=True)
    g12EnCredit = Column(String(50), nullable=True)
    g12EnTitle = Column(String(50), nullable=True)
    docCopyTrans = Column(LONGTEXT, nullable=True)
    docCopyName = Column(String(255), nullable=True)
    docCopySize = Column(String(50), nullable=True)