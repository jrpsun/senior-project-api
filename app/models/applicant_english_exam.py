from sqlalchemy import Column, String, ForeignKey
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations


class ApplicantEnglishExam(Base):
    __tablename__ = 'Applicant_English_Exam'

    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    examType = Column(String(50), nullable=True)
    enScore = Column(String(50), nullable=True)
    enExamDate = Column(String(50), nullable=True)
    listening = Column(String(50), nullable=True)
    speaking = Column(String(50), nullable=True)
    reading = Column(String(50), nullable=True)
    writing = Column(String(50), nullable=True)
    literacy = Column(String(50), nullable=True)
    comprehension = Column(String(50), nullable=True)
    conversation = Column(String(50), nullable=True)
    production = Column(String(50), nullable=True)
    listeningComprehensionScore = Column(String(50), nullable=True)
    structureWrittenScore = Column(String(50), nullable=True)
    readingComprehensionScore = Column(String(50), nullable=True) 
    enCer = Column(LONGTEXT, nullable=True)
    enCerName = Column(String(255), nullable=True)
    enCerSize = Column(String(50), nullable=True)