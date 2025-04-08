from pydantic import BaseModel
from typing import Optional


class EducationDepartmentBase(BaseModel):
    educationId: str
    prefix: str
    firstName: str
    lastName: str
    username: str
    email: str
    phoneNumber: str


class EducationDepartmentCreate(EducationDepartmentBase):
    password: str


class EducationDepartmentUpdate(BaseModel):
    prefix: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None
    password: Optional[str] = None


class EducationDepartmentResponse(EducationDepartmentBase):
    lastSeen: Optional[str] = None

    class Config:
        from_attributes = True



class EduApplicantDataMainPageResponse(BaseModel):
    roundName: Optional[str] = None
    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    program: Optional[str] = None
    admissionStatus: Optional[str] = None
    docStatus: Optional[str] = None
    paymentStatus: Optional[str] = None
    applicantEmail: Optional[str] = None
    applicantPhone: Optional[str] = None

    class Config:
        from_attributes = True


class EduListApplicantDataMainPageResponse(BaseModel):
    applicants: list[EduApplicantDataMainPageResponse]


class AdminRolePageResponse(BaseModel):
    prefix: Optional[str] = None 
    firstName: Optional[str] = None 
    lastName: Optional[str] = None 
    email: Optional[str] = None 
    phoneNumber: Optional[str] = None 
    roles: list[str] 
    lastSeen: Optional[str] = None


class AdminRoleListPageResponse(BaseModel):
    admins: list[AdminRolePageResponse]


class SummaryInterviewPageResponse(BaseModel):
    interviewStatus: Optional[str] = None

    interviewRoom: Optional[str] = None 
    englishScore: Optional[int] = None 
    personalityScore: Optional[int] = None 
    intensionScore: Optional[int] = None 
    computerScore: Optional[int] = None 
    totalScore: Optional[int] = None
    
    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    programRegistered: Optional[str] = None

    program: Optional[str] = None
    roundName: Optional[str] = None

    InterviewCommittee: list[str]


class SummaryInterviewListPageResponse(BaseModel):
    applicants: list[SummaryInterviewPageResponse]