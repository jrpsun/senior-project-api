from sqlalchemy import Column, String, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantEnglishExam(Base):
    __tablename__ = 'Applicant_English_Exam'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    examType = Column(String(50), nullable=True)
    enScore = Column(Float, nullable=True)
    enExamDate = Column(String(50), nullable=True)
    listening = Column(Float, nullable=True)
    speaking = Column(Float, nullable=True)
    reading = Column(Float, nullable=True)
    writing = Column(Float, nullable=True)
    literacy = Column(Float, nullable=True)
    comprehension = Column(Float, nullable=True)
    conversation = Column(Float, nullable=True)
    production = Column(Float, nullable=True)
    enCer = Column(LONGTEXT, nullable=True)