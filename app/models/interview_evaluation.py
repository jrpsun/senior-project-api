from sqlalchemy import Column, String, Text, ForeignKey, Integer
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.interview_committee import InterviewCommittee


class InterviewEvaluation(Base):
    __tablename__ = 'Interview_Evaluation'

    interviewEvald = Column(String(50), primary_key=True)
    interviewComId = Column(String(50), ForeignKey('Interview_Committee.interviewComId'))
    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'))
    englishScore = Column(Integer)
    personalityScore = Column(Integer)
    intensionScore = Column(Integer)
    computerScore = Column(Integer)
    totalScore = Column(Integer)
    comment = Column(Text)
    interviewRoom = Column(String(255))
    interviewDate = Column(String(50))
    interviewTime = Column(String(50))