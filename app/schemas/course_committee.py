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
    username: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None
    password: Optional[str] = None


class CourseCommitteeResponse(CourseCommitteeBase):
    lastSeen: Optional[str] = None

    class Config:
        from_attributes = True