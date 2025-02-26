from sqlalchemy import Column, String, Date, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicanntAcademicBackgroundTypeA(Base):
    __tablename__ = 'Applicant_Academic_Background_TypeA'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    currentStatus = Column(String(50))
    graduateDate = Column(Date)
    country = Column(String(50))
    province = Column(String(50))
    schoolName = Column(String(100))
    studyPlan = Column(String(100))
    cumulativeGPA = Column(Float)
    english = Column(Float)
    mathematics = Column(Float)
    scitech = Column(Float)
    docCopyTrans = Column(LONGTEXT)