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
    applicantEmail: str


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
    applicantPhone: Optional[str] = None
    applicantEmail: Optional[str] = None
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
    contactFirstNameTH: Optional[str] = None
    contactMiddleNameTH: Optional[str] = None
    contactLastNameTH: Optional[str] = None
    contactFirstNameEN: Optional[str] = None
    contactMiddleNameEN: Optional[str] = None
    contactLastNameEN: Optional[str] = None
    relationship: Optional[str] = None
    contactPhone: Optional[str] = None
    contactEmail: Optional[str] = None
    # AdmissionChannel
    onlineChannel: Optional[str] = None
    offlineChannel: Optional[str] = None


class GeneralInfoWithAddress(BaseModel):
    # GeneralInfo
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

    # AddressInfo
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


class ContactInfo(BaseModel):
    applicantPhone: Optional[str] = None
    applicantEmail: Optional[str] = None
    line: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None


class EmergencyContact(BaseModel):
    contactFirstNameTH: Optional[str] = None
    contactMiddleNameTH: Optional[str] = None
    contactLastNameTH: Optional[str] = None
    contactFirstNameEN: Optional[str] = None
    contactMiddleNameEN: Optional[str] = None
    contactLastNameEN: Optional[str] = None
    relationship: Optional[str] = None
    contactPhone: Optional[str] = None
    contactEmail: Optional[str] = None


class AdmissionChannel(BaseModel):
    onlineChannel: Optional[str] = None
    offlineChannel: Optional[str] = None


class ApplicantGeneralInformationResponse(BaseModel):
    general_info: GeneralInfoWithAddress
    contact_info: ContactInfo
    emergency_contact: EmergencyContact
    admission_channel: AdmissionChannel



class ApplicantEducationinfoUpdate(BaseModel):
    # Background
    academicType: Optional[str] = None
    currentStatus: Optional[str] = None
    graduateDate: Optional[str] = None
    academicCountry: Optional[str] = None
    academicProvince: Optional[str] = None
    schoolName: Optional[str] = None
    studyPlan: Optional[str] = None
    cumulativeGPA: Optional[float] = None
    dstEnglish: Optional[float] = None
    dstMathematics: Optional[float] = None
    dstScitech: Optional[float] = None
    comSciTitle: Optional[str] = None
    comSciCredit: Optional[float] = None
    gedMathematics: Optional[float] = None
    gedScience: Optional[float] = None
    gedSocialStudies: Optional[float] = None
    gedLanguageArts: Optional[float] = None
    g12MathCredit: Optional[float] = None
    g12MathTitle: Optional[str] = None
    g12SciCredit: Optional[float] = None
    g12SciTitle: Optional[str] = None
    g12EnCredit: Optional[float] = None
    g12EnTitle: Optional[str] = None
    # EngExam
    examType: Optional[str] = None
    enScore: Optional[float] = None
    enExamDate: Optional[str] = None
    listening: Optional[float] = None
    speaking: Optional[float] = None
    reading: Optional[float] = None
    writing: Optional[float] = None
    literacy: Optional[float] = None
    comprehension: Optional[float] = None
    conversation: Optional[float] = None
    production:Optional[float] = None
    # MathExam
    mathType: Optional[str] = None
    mathScore: Optional[float] = None
    mathExamDate: Optional[str] = None


class ApplicantEducationInfoResponse(ApplicantEducationinfoUpdate):
    
    class Config:
        from_attributes = True


class ApplicantAdminDashboardResponse(BaseModel):
    applicantId: Optional[str] = None
    applicantName: Optional[str] = None
    programRegistered: Optional[str] = None
    program: Optional[str] = None
    submissionStatus: Optional[bool] = None
    docStatus: Optional[str] = None
    paymentStatus: Optional[str] = None
    applicantEmail: Optional[str] = None
    applicantPhone: Optional[str] = None

    class Config:
        from_attributes = True

class ApplicantListAdminDashboardResponse(BaseModel):
    applicants: list[ApplicantAdminDashboardResponse]
