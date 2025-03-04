from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class InterviewCommitteeBase(BaseModel):
    interviewComId: str
    prefix: str
    firstName: str
    lastName: str
    username: str
    email: str
    phoneNumber: str


class InterviewCommitteeCreate(InterviewCommitteeBase):
    password: str


class InterviewCommitteeUpdate(BaseModel):
    prefix: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None


class InterviewCommitteeResponse(InterviewCommitteeBase):
    lastSeen: Optional[str] = None

    class Config:
        from_attributes = True