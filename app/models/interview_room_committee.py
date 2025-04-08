from sqlalchemy import Column, String, Text, ForeignKey, Integer
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
import uuid
from app.models.interview_committee import InterviewCommittee
from app.models.interview_room_details import InterviewRoomDetails

class InterviewRoomCommittee(Base):
    __tablename__ = "Interview_Room_Committee"

    InterviewRoomCommitteeId = Column(String(50), primary_key=True, default=uuid.uuid4)
    interviewRoomId = Column(String(50), ForeignKey('Interview_Room_Details.interviewRoomId'))
    interviewComId = Column(String(50), ForeignKey('Interview_Committee.interviewComId'))