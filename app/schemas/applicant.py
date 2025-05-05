from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, File


class ApplicantInfoProfile(BaseModel):
    nationality: str
    idCardNumber: Optional[str] = None
    passportId: Optional[str] = None
    prefix: str
    firstnameTH: Optional[str] = None
    lastnameTH: Optional[str] = None
    firstnameEN: str
    lastnameEN: str
    applicantEmail: str


class ApplicantEditProfile(BaseModel):
    prefix: str
    firstNameTH: str
    lastNameTH: str
    firstNameEN: str
    lastNameEN: str
    email: str



class ApplicantGeneralInformationUpdate(BaseModel):
    # GeneralInformation
    #nationality: Optional[str] = None
    #idCardNumber: Optional[str] = None
    #passportId: Optional[str] = None
    #prefix: Optional[str] = None
    #firstnameTH: Optional[str] = None
    #lastnameTH: Optional[str] = None
    #firstnameEN: Optional[str] = None
    #lastnameEN: Optional[str] = None
    idCardExpDate: Optional[str] = None
    passportExpDate: Optional[str] = None
    gender: Optional[str] = None
    middlenameTH: Optional[str] = None
    middlenameEN: Optional[str] = None
    nicknameTH: Optional[str] = None
    nicknameEN: Optional[str] = None
    birthDate: Optional[str] = None
    livingCountry: Optional[str] = None
    applicantPicture: Optional[str] = None
    docCopyIdCard: Optional[str] = None
    docCopyIdCardName: Optional[str] = None
    docCopyIdCardSize: Optional[str] = None
    docCopyPassport: Optional[str] = None
    docCopyPassportName: Optional[str] = None
    docCopyPassportSize: Optional[str] = None
    docCopyHouseRegis: Optional[str] = None
    docCopyHouseRegisName: Optional[str] = None
    docCopyHouseRegisSize: Optional[str] = None
    # ContactApplicant
    applicantPhone: Optional[str] = None
    #applicantEmail: Optional[str] = None
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
    applicantPicture: Optional[str] = None
    docCopyIdCard: Optional[str] = None
    docCopyIdCardName: Optional[str] = None
    docCopyIdCardSize: Optional[str] = None
    docCopyPassport: Optional[str] = None
    docCopyPassportName: Optional[str] = None
    docCopyPassportSize: Optional[str] = None
    docCopyHouseRegis: Optional[str] = None
    docCopyHouseRegisName: Optional[str] = None
    docCopyHouseRegisSize: Optional[str] = None

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
    graduateYear: Optional[str] = None
    academicCountry: Optional[str] = None
    academicProvince: Optional[str] = None
    schoolName: Optional[str] = None
    studyPlan: Optional[str] = None
    customAcademicType: Optional[str] = None
    customStudyPlan: Optional[str] = None
    cumulativeGPA: Optional[str] = None
    dstEnglish: Optional[str] = None
    dstMathematics: Optional[str] = None
    dstScitech: Optional[str] = None
    comSciTitle: Optional[str] = None
    comSciCredit: Optional[str] = None
    gedMathematics: Optional[str] = None
    gedScience: Optional[str] = None
    gedSocialStudies: Optional[str] = None
    gedLanguageArts: Optional[str] = None
    g12MathCredit: Optional[str] = None 
    g12MathTitle: Optional[str] = None
    g12SciCredit: Optional[str] = None
    g12SciTitle: Optional[str] = None
    g12EnCredit: Optional[str] = None
    g12EnTitle: Optional[str] = None
    docCopyTrans: Optional[str] = None
    docCopyName: Optional[str] = None
    docCopySize: Optional[str] = None
    # EngExam
    examType: Optional[str] = None
    enScore: Optional[str] = None
    enExamDate: Optional[str] = None
    listening: Optional[str] = None
    speaking: Optional[str] = None
    reading: Optional[str] = None
    writing: Optional[str] = None
    literacy: Optional[str] = None
    comprehension: Optional[str] = None
    conversation: Optional[str] = None
    production:Optional[str] = None
    listeningComprehensionScore:Optional[str] = None
    structureWrittenScore:Optional[str] = None
    readingComprehensionScore:Optional[str] = None
    enCer: Optional[str] = None
    enCerName: Optional[str] = None
    enCerSize: Optional[str] = None
    # MathExam
    mathType: Optional[str] = None
    mathScore: Optional[str] = None
    mathExamDate: Optional[str] = None
    mathCer: Optional[str] = None
    mathCerName: Optional[str] = None
    mathCerSize: Optional[str] = None


class ApplicantEducationBackground(BaseModel):
    academicType: Optional[str] = None
    customAcademicType: Optional[str] = None
    currentStatus: Optional[str] = None
    graduateDate: Optional[str] = None
    graduateYear: Optional[str] = None
    academicCountry: Optional[str] = None
    academicProvince: Optional[str] = None
    schoolName: Optional[str] = None
    studyPlan: Optional[str] = None
    customStudyPlan: Optional[str] = None
    cumulativeGPA: Optional[str] = None
    dstEnglish: Optional[str] = None
    dstMathematics: Optional[str] = None
    dstScitech: Optional[str] = None
    comSciTitle: Optional[str] = None
    comSciCredit: Optional[str] = None
    gedMathematics: Optional[str] = None
    gedScience: Optional[str] = None
    gedSocialStudies: Optional[str] = None
    gedLanguageArts: Optional[str] = None
    g12MathCredit: Optional[str] = None
    g12MathTitle: Optional[str] = None
    g12SciCredit: Optional[str] = None
    g12SciTitle: Optional[str] = None
    g12EnCredit: Optional[str] = None
    g12EnTitle: Optional[str] = None
    docCopyTrans: Optional[str] = None
    docCopyName: Optional[str] = None
    docCopySize: Optional[str] = None


class ApplicantEducationEngExam(BaseModel):
    examType: Optional[str] = None
    enScore: Optional[str] = None
    enExamDate: Optional[str] = None
    listening: Optional[str] = None
    speaking: Optional[str] = None
    reading: Optional[str] = None
    writing: Optional[str] = None
    literacy: Optional[str] = None
    comprehension: Optional[str] = None
    conversation: Optional[str] = None
    production: Optional[str] = None
    listeningComprehensionScore: Optional[str] = None
    structureWrittenScore: Optional[str] = None
    readingComprehensionScore: Optional[str] = None
    enCer: Optional[str] = None
    enCerName: Optional[str] = None
    enCerSize: Optional[str] = None


class ApplicantEducationMathExam(BaseModel):
    mathType: Optional[str] = None
    mathScore: Optional[str] = None
    mathExamDate: Optional[str] = None
    mathCer: Optional[str] = None
    mathCerName: Optional[str] = None
    mathCerSize: Optional[str] = None


class ApplicantEducationInfoResponse(BaseModel):
    background: ApplicantEducationBackground
    eng_exam: ApplicantEducationEngExam
    math_exam: ApplicantEducationMathExam

    class Config:
        from_attributes = True


# Reward
class ApplicantRewardResponse(BaseModel):
    rewardId: Optional[str] = None
    applicantId: Optional[str] = None
    programRegistered: Optional[str] = None
    nameOfCompetition: Optional[str] = None
    rewardYear: Optional[str] = None
    rewardLevel: Optional[str] = None
    rewardAwards: Optional[str] = None
    project: Optional[str] = None
    rewardCer: Optional[str] = None
    rewardCerName: Optional[str] = None
    rewardCerSize: Optional[str] = None


# Talent
class ApplicantTalentResponse(BaseModel):
    talentId: Optional[str] = None
    applicantId: Optional[str] = None
    programRegistered: Optional[str] = None
    kindOfTalent: Optional[str] = None
    nameOfCompetition: Optional[str] = None
    talentYear: Optional[str] = None
    talentAwards: Optional[str] = None
    url: Optional[str] = None
    moreDetails: Optional[str] = None
    talentCer: Optional[str] = None
    talentCerName: Optional[str] = None
    talentCerSize: Optional[str] = None


# Training
class ApplicantTrainingResponse(BaseModel):
    trainingId: Optional[str] = None
    applicantId: Optional[str] = None
    programRegistered: Optional[str] = None
    nameOfCourse: Optional[str] = None
    institution: Optional[str] = None
    trainingYear: Optional[str] = None
    trainingMode: Optional[str] = None
    trainingCountry: Optional[str] = None
    trainingCer: Optional[str] = None
    trainingCerName: Optional[str] = None
    trainingCerSize: Optional[str] = None


# Documents
class ApplicantDocumentsResponse(BaseModel):
    stateOfPurpose: Optional[str] = None
    stateOfPurposeName: Optional[str] = None
    stateOfPurposeSize: Optional[str] = None
    portfolio: Optional[str] = None
    portfolioName: Optional[str] = None
    portfolioSize: Optional[str] = None
    vdo: Optional[str] = None
    applicantResume: Optional[str] = None
    applicantResumeName: Optional[str] = None
    applicantResumeSize: Optional[str] = None
    additional: Optional[str] = None
    additionalName: Optional[str] = None
    additionalSize: Optional[str] = None


class ApplicantRegistrationsResponse(BaseModel):
    idCardNumber: Optional[str] = None
    passportId: Optional[str] = None
    applicantEmail: str
    prefix: str
    firstnameTH: Optional[str] = None
    firstnameEN: str
    lastnameTH: Optional[str] = None
    lastnameEN: str
    nationality: str

    class Config:
        from_attributes = True


class ApplicantCancel(BaseModel):
    applicantId: str
    admissionId: str
    reason: Optional[str] = None
    details: Optional[str] = None