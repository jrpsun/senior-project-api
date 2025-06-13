from sqlalchemy import Column, String, Text, ForeignKey, Integer
import uuid
from app.db import Base
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations
from app.models.interview_committee import InterviewCommittee
from app.models.interview_round import InterviewRound
import uuid


class InterviewEvaluation(Base):
    __tablename__ = 'Interview_Evaluation'

    interviewEvald = Column(String(50), primary_key=True, default=uuid.uuid4)
    interviewComId = Column(String(50), ForeignKey('Interview_Committee.interviewComId'))
    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'))
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'))
    interviewRoundId = Column(String(50), ForeignKey('Interview_Round.interviewRoundId'))
    educationId = Column(String(50), ForeignKey('Education_Department.educationId'))
    englishScore = Column(Integer, nullable=True)
    personalityScore = Column(Integer, nullable=True)
    intensionScore = Column(Integer, nullable=True)
    computerScore = Column(Integer, nullable=True)
    totalScore = Column(Integer, nullable=True)
    comment = Column(Text, nullable=True)
    interviewRoom = Column(String(255), nullable=True)
    interviewDate = Column(String(50), nullable=True)
    interviewTime = Column(String(50), nullable=True)
    interviewResult = Column(String(255), nullable=True)
    englishRemark = Column(String(255), nullable=True)
    personalityRemark = Column(String(255), nullable=True)
    intensionRemark = Column(String(255), nullable=True)
    computerRemark = Column(String(255), nullable=True)
    totalRemark = Column(String(255), nullable=True)
    outstandingLevel = Column(String(10), nullable=True)
    evaDate = Column(String(50), nullable=True)
    