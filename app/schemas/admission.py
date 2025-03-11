from pydantic import BaseModel
from typing import Optional


class AdmissionBase(BaseModel):
    admissionId: str
    program: str
    roundName: str
    academicYear: str
    startDate: str
    endDate: str


class AdmissionUpdate(BaseModel):
    program: Optional[str] = None
    roundName: Optional[str] = None
    academicYear: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None


class AdmissionResponse(AdmissionBase):

    class Config:
        from_attributes = True