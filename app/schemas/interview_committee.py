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
    interviewStatus: Optional[str] = None
    interviewRoom: Optional[str] = None
    prefix1: Optional[str] = None
    firstName1: Optional[str] = None
    lastName1: Optional[str] = None
    prefix2: Optional[str] = None
    firstName2: Optional[str] = None
    lastName2: Optional[str] = None
    interviewDate: Optional[str] = None 
    interviewTime: Optional[str] = None 
  #  interviewResult: Optional[str] = None 

    class Config:
        from_attributes = True


class InterviewListApplicantDataMainPageResponse(BaseModel):
    applicants: list[InterviewApplicantDataMainPageResponse]


class InterviewEvaPageResponse(BaseModel):
    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    admissionStatus: Optional[str] = None
    comPrefix: Optional[str] = None 
    firstName: Optional[str] = None
    interviewDate: Optional[str] = None
    interviewTime: Optional[str] = None
    interviewResult: Optional[str] = None
    englishScore: Optional[int] = None
    personalityScore: Optional[int] = None
    intensionScore: Optional[int] = None
    computerScore: Optional[int] = None
    totalScore: Optional[int] = None
    englishRemark : Optional[str] = None  
    personalityRemark : Optional[str] = None
    intensionRemark : Optional[str] = None
    computerRemark : Optional[str] = None
    totalRemark : Optional[str] = None
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class InterviewEvaListPageResponse(BaseModel):
    applicants: list[InterviewEvaPageResponse]


class InterviewEvaUpdate(BaseModel):
    englishScore: int
    personalityScore: int
    intensionScore: int
    computerScore: int
    totalScore: int
    englishRemark : Optional[str] = None  
    personalityRemark : Optional[str] = None
    intensionRemark : Optional[str] = None
    computerRemark : Optional[str] = None
    totalRemark : Optional[str] = None
    comment: Optional[str] = None
    interviewResult: Optional[str] = None
    committee: list[str]


class InterviewEvaCreate(BaseModel):
    applicantId: str 
    room: str
    intDate: str
    intTime: str
    committeeId: list[str]


class InterviewRoundCreate(BaseModel):
    admissionProgram: Optional[str] = None 
    admissionRoundName: Optional[str] = None 
    interviewDate: Optional[str] = None 
    startTime: Optional[str] = None 
    endTime: Optional[str] = None 
    duration: Optional[str] = None 


class InterviewRoomCreate(BaseModel):
    interviewRoundId: Optional[str] = None
    interviewRoom: Optional[str] = None
    interviewType: Optional[str] = None
    interviewComId: list[str]


class InterviewRoomUpdate(BaseModel):
    interviewRoundId: Optional[str] = None
    interviewRoom: Optional[str] = None
    interviewType: Optional[str] = None
    interviewDate: Optional[str] = None
    startTime: Optional[str] = None 
    endTime: Optional[str] = None 
    duration: Optional[str] = None
    interviewComId: list[str]