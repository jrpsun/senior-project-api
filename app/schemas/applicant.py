from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, File



class ApplicantBase(BaseModel):
    applicantId: str
    nationality: str
    idCardNumber: Optional[str] = None
    passportId: Optional[str] = None
    prefix: str
    firstnameTH: Optional[str] = None
    lastnameTH: Optional[str] = None
    firstnameEN: str
    lastnameEN: str
    email: str


class ApplicantCreate(ApplicantBase):
    password: str


class ApplicantGeneralInformationUpdate(BaseModel):
    # GeneralInformation
    nationality: Optional[str] = None
    idCardNumber: Optional[str] = None
    passportId: Optional[str] = None
    prefix: Optional[str] = None
    firstnameTH: Optional[str] = None
    lastnameTH: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    idCardExpDate: Optional[str] = None
    passportExpDate: Optional[str] = None
    gender: Optional[str] = None
    middlenameTH: Optional[str] = None
    middlenameEN: Optional[str] = None
    nicknameTH: Optional[str] = None
    nicknameEN: Optional[str] = None
    birthDate: Optional[str] = None
    livingCountry: Optional[str] = None
    # ContactApplicant
    applicantPhoneNumber: Optional[str] = None
    line: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    # AddressThai
    houseNumber: Optional[str] = None
    moo: Optional[str] = None
    subDistrict: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    postalCode: Optional[str] = None
    village: Optional[str] = None
    soi: Optional[str] = None
    street: Optional[str] = None
    addr1: Optional[str] = None
    addr2: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    # ContactPerson
    thName: Optional[str] = None
    enName: Optional[str] = None
    relationship: Optional[str] = None
    contactPhoneNumber: Optional[str] = None
    contactEmail: Optional[str] = None
    # AdmissionChannel
    onlineChannel: Optional[str] = None
    offlineChannel: Optional[str] = None


class ApplicantGeneralInformationResponse(ApplicantGeneralInformationUpdate):
    
    class Config:
        from_attributes = True