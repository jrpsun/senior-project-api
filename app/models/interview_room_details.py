from sqlalchemy import Column, String, Text, ForeignKey, Integer
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
import uuid
from app.models.interview_round import InterviewRound

class InterviewRoomDetails(Base):
    __tablename__ = "Interview_Room_Details"

    interviewRoomId = Column(String(50), primary_key=True, default=uuid.uuid4)
    interviewRoundId = Column(String(50), ForeignKey('Interview_Round.interviewRoundId'))
    interviewRoom = Column(String(50))
    interviewType = Column(String(50)) 