from sqlalchemy import Column, String, Text, ForeignKey, Integer
import uuid
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.interview_committee import InterviewCommittee
from app.models.interview_round import InterviewRound
import uuid


class InterviewEvaluation(Base):
    __tablename__ = 'Interview_Evaluation'

    interviewEvald = Column(String(50), primary_key=True, default=uuid.uuid4)
    interviewComId = Column(String(50), ForeignKey('Interview_Committee.interviewComId'))
    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'))
    interviewRoundId = Column(String(50), ForeignKey('Interview_Round.interviewRoundId'))
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