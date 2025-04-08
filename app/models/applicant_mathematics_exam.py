from sqlalchemy import Column, String, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantMathematicsExam(Base):
    __tablename__ = 'Applicant_Mathematics_Exam'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    mathType = Column(String(50), nullable=True)
    mathScore = Column(String(50), nullable=True)
    mathExamDate = Column(String(50), nullable=True)
    mathCer = Column(LONGTEXT, nullable=True)
    mathCerName = Column(String(255), nullable=True)
    mathCerSize = Column(String(50), nullable=True)