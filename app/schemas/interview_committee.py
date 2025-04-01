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


class InterviewApplicantDataMainPageResponse(BaseModel):
    roundName: Optional[str] = None
    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    program: Optional[str] = None
    admissionStatus: Optional[str] = None
    docStatus: Optional[str] = None
    interviewRoom: Optional[str] = None
    prefix: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    interviewDate: Optional[str] = None 
    interviewTime: Optional[str] = None 

    class Config:
        from_attributes = True


class InterviewListApplicantDataMainPageResponse(BaseModel):
    applicants: list[InterviewApplicantDataMainPageResponse]