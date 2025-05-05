from sqlalchemy import Column, String
from app.db import Base


class CourseCommittee(Base):
    __tablename__ = 'Course_Committee'

    courseComId = Column(String(50), primary_key=True)
    prefix = Column(String(50))
    firstName = Column(String(50))
    lastName = Column(String(50))
    username = Column(String(50))
    password = Column(String(255))
    email = Column(String(50))
    lastSeen = Column(String(50), nullable=True)
    phoneNumber = Column(String(50))
