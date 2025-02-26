from sqlalchemy import Column, String, Date, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantMathematicsExam(Base):
    __tablename__ = 'Applicant_Mathematics_Exam'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    mathType = Column(String(50))
    score = Column(Float)
    examDate = Column(Date)
    mathCer = Column(LONGTEXT)