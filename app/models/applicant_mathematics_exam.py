from sqlalchemy import Column, String, ForeignKey
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations


class ApplicantMathematicsExam(Base):
    __tablename__ = 'Applicant_Mathematics_Exam'

    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    mathType = Column(String(50), nullable=True)
    mathScore = Column(String(50), nullable=True)
    mathExamDate = Column(String(50), nullable=True)
    mathCer = Column(LONGTEXT, nullable=True)
    mathCerName = Column(String(255), nullable=True)
    mathCerSize = Column(String(50), nullable=True)