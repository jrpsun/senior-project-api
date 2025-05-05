from pydantic import BaseModel
from typing import Optional


class ApplicantFilterExcel(BaseModel):
    course: Optional[str] = None
    round: Optional[str] = None
    year: Optional[str] = None
    admitStatus: Optional[str] = None
    docStatus: Optional[str] = None
    paymentStatus: Optional[str] = None


class ApplicantFilterCourseSummary(BaseModel):
    course: Optional[str] = None
    round: Optional[str] = None
    year: Optional[str] = None
    committee: Optional[str] = None
    result: Optional[str] = None