from sqlalchemy import Column, String, Text, ForeignKey, Integer
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
import uuid

class InterviewRound(Base):
    __tablename__ = "Interview_Round"

    interviewRoundId = Column(String(50), primary_key=True, default=uuid.uuid4)
    admissionProgram = Column(String(255))
    admissionRoundName = Column(String(255))
    interviewDate = Column(String(50))
    startTime = Column(String(50))
    endTime = Column(String(50))
    duration = Column(String(50))