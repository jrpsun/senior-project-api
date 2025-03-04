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
