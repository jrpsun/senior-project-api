from sqlalchemy import Column, String, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantAcademicBackgroundTypeC(Base):
    __tablename__ = 'Applicant_Academic_Background_TypeC'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    currentStatus = Column(String(50), nullable=True)
    graduateDate = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    province = Column(String(50), nullable=True)
    schoolName = Column(String(50), nullable=True)
    studyPlan = Column(String(50), nullable=True)
    mathCredit = Column(Float, nullable=True)
    mathTitle = Column(String(50), nullable=True)
    sciCredit = Column(Float, nullable=True)
    sciTitle = Column(String(50), nullable=True)
    enCredit = Column(Float, nullable=True)
    enTitle = Column(String(50), nullable=True)
    docCopyTrans = Column(LONGTEXT, nullable=True)