from pydantic import BaseModel
from typing import Optional


class CourseCommitteeBase(BaseModel):
    courseComId: str
    prefix: str
    firstName: str
    lastName: str
    username: str
    email: str
    phoneNumber: str


class CourseCommitteeCreate(CourseCommitteeBase):
    password: str


class CourseCommitteeUpdate(BaseModel):
    prefix: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None


class CourseCommitteeResponse(CourseCommitteeBase):
    lastSeen: Optional[str] = None

    class Config:
        from_attributes = True


class CourseApplicantDataMainPageResponse(BaseModel):
    roundName: Optional[str] = None
    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    fullnameEN: Optional[str] = None
    program: Optional[str] = None
    admissionStatus: Optional[str] = None
    docStatus: Optional[str] = None
    paymentStatus: Optional[str] = None
    courseComId: Optional[str] = None
    prefix: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    preEvaDate : Optional[str] = None
    preliminaryEva: Optional[str] = None
    preliminaryComment: Optional[str] = None

    class Config:
        from_attributes = True


class CourseListApplicantDataMainPageResponse(BaseModel):
    applicants: list[CourseApplicantDataMainPageResponse]


class PreEvaPageResponse(BaseModel):
    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    comPrefix: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    preEvaDate: Optional[str] = None
    preliminaryEva: Optional[str] = None
    preliminaryComment: Optional[str] = None


class PreEvaRequest(BaseModel):
    app_id: str
    com_id: str
    preEvaResult: str
    comment: Optional[str] = None
    preEvaDate: str