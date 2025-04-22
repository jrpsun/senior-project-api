from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, File



class ApplicantCreate(BaseModel):
    idNumber: str
    idType: str
    email: str
    title: str
    firstNameEnglish: str
    firstNameThai: Optional[str] = None
    lastNameEnglish: str
    lastNameThai: Optional[str] = None
    nationality: str
    password: str


class ApplicantLoginRequest(BaseModel):
    idNumber: str
    password: str


class AdminLoginRequest(BaseModel):
    email: str
    password: str