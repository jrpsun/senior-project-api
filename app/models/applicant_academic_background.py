from sqlalchemy import Column, String, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantAcademicBackground(Base):
    __tablename__ = 'Applicant_Academic_Background'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    academicType = Column(String(50), nullable=True)
    currentStatus = Column(String(50), nullable=True)
    graduateDate = Column(String(50), nullable=True)
    academicCountry = Column(String(50), nullable=True)
    academicProvince = Column(String(50), nullable=True)
    schoolName = Column(String(100), nullable=True)
    studyPlan = Column(String(100), nullable=True)
    cumulativeGPA = Column(Float, nullable=True)
    dstEnglish = Column(Float, nullable=True)
    dstMathematics = Column(Float, nullable=True)
    dstScitech = Column(Float, nullable=True)
    comSciTitle = Column(String(50), nullable=True)
    comSciCredit = Column(Float, nullable=True)
    gedMathematics = Column(Float, nullable=True)
    gedScience = Column(Float, nullable=True)
    gedSocialStudies = Column(Float, nullable=True)
    gedLanguageArts = Column(Float, nullable=True)
    g12MathCredit = Column(Float, nullable=True)
    g12MathTitle = Column(String(50), nullable=True)
    g12SciCredit = Column(Float, nullable=True)
    g12SciTitle = Column(String(50), nullable=True)
    g12EnCredit = Column(Float, nullable=True)
    g12EnTitle = Column(String(50), nullable=True)
    docCopyTrans = Column(LONGTEXT, nullable=True)