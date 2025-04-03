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
