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
    email: Optional[str] = None
    phoneNumber: Optional[str] = None


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
    reason: Optional[str] = None
    moreDetail: Optional[str] = None

    class Config:
        from_attributes = True


class EduListApplicantDataMainPageResponse(BaseModel):
    applicants: list[EduApplicantDataMainPageResponse]


class AdminRolePageResponse(BaseModel):
    adminId: Optional[str] = None
    prefix: Optional[str] = None 
    firstName: Optional[str] = None 
    lastName: Optional[str] = None 
    email: Optional[str] = None 
    phoneNumber: Optional[str] = None 
    roles: list[str] 
    lastSeen: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class AdminRoleListPageResponse(BaseModel):
    admins: list[AdminRolePageResponse]


class CommitteeResult(BaseModel):
    id: Optional[str]
    shortName: Optional[str]
    name: Optional[str]
    InterviewResult: Optional[str]


class SummaryInterviewPageResponse(BaseModel):
    interviewStatus: Optional[str] = None
    admissionStatus: Optional[str] = None
    docStatus: Optional[str] = None
    paymentStatus: Optional[str] = None
    interviewRoom: Optional[str] = None 
    interviewDate: Optional[str] = None
    interviewTime: Optional[str] = None
    englishScore: Optional[int] = None 
    personalityScore: Optional[int] = None 
    intensionScore: Optional[int] = None 
    computerScore: Optional[int] = None 
    totalScore: Optional[int] = None

    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    fullnameEN: Optional[str] = None
    programRegistered: Optional[str] = None

    program: Optional[str] = None
    roundName: Optional[str] = None

    InterviewCommittee: list[CommitteeResult] = []



class SummaryInterviewListPageResponse(BaseModel):
    applicants: list[SummaryInterviewPageResponse]


class PreEvaUpdateApplicantModel(BaseModel):
    app_id: str
    com_id: str


class EduInterviewEvaResponse(BaseModel):
    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    interviewComId: Optional[str] = None
    prefix: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    interviewRoom: Optional[str] = None
    interviewDate: Optional[str] = None
    interviewTime: Optional[str] = None
    englishScore: Optional[int] = None
    personalityScore: Optional[int] = None
    intensionScore: Optional[int] = None
    computerScore: Optional[int] = None
    totalScore: Optional[int] = None
    englishRemark: Optional[str] = None
    personalityRemark: Optional[str] = None
    intensionRemark: Optional[str] = None
    computerRemark: Optional[str] = None
    totalRemark: Optional[str] = None
    comment: Optional[str] = None
    interviewResult: Optional[str] = None


class EduInterviewEvaListResponse(BaseModel):
    applicants: list[EduInterviewEvaResponse]


class InterviewRoundResponse(BaseModel):
    interviewRoundId: Optional[str] = None
    admissionProgram: Optional[str] = None
    admissionRoundName: Optional[str] = None
    interviewDate: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    duration: Optional[str] = None


class InterviewRoundListResponse(BaseModel):
    interviewRound: list[InterviewRoundResponse]


class InterviewRoundUpdate(BaseModel):
    admissionProgram: Optional[str] = None
    admissionRoundName: Optional[str] = None
    interviewDate: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    duration: Optional[str] = None


class InterviewRoomDetailCreating(BaseModel):
    interviewRoomId: Optional[str] = None
    interviewRoundId: Optional[str] = None
    interviewRoom: Optional[str] = None
    interviewType: Optional[str] = None


class InterviewRoomCommitteeCreating(BaseModel):
    interviewRoomId: Optional[str] = None
    interviewComId: list[str]


class InterviewRoomCommitteeResponse(BaseModel):
    InterviewRoomCommitteeId: Optional[str] = None
    interviewRoomId: Optional[str] = None
    interviewComId: Optional[str] = None


class InterviewCommitteeMember(BaseModel):
    interviewComId: Optional[str] = None
    prefix: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None


class InterviewRoundDetailResponse(BaseModel):
    interviewRoundId: Optional[str] = None
    interviewDate: Optional[str] = None
    interviewStartTime: Optional[str] = None
    interviewEndTime: Optional[str] = None
    admissionProgram: Optional[str] = None
    admissionRoundName: Optional[str] = None

    interviewRoomId: Optional[str] = None
    interviewRoom: Optional[str] = None
    interviewType: Optional[str] = None
    
    interviewComs: list[InterviewCommitteeMember] = []


class InterviewRoundDetailListResponse(BaseModel):
    details: list[InterviewRoundDetailResponse]
    
    
class InterviewRoomCommitteeUpdateRequest(BaseModel):
    interviewRoomId: Optional[str] = None
    interviewComId: Optional[list[str]] = None


class InterviewRoomDetailsResponse(BaseModel):
    interviewRoomId: Optional[str] = None 
    interviewRoom: Optional[str] = None 
    interviewComs: list[InterviewCommitteeMember] = []
    interviewRoundId: Optional[str] = None
    interviewDate: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    duration: Optional[str] = None


class InterviewRoomDetailsListResponse(BaseModel):
    room: list[InterviewRoomDetailsResponse]
class EduApplicantDataViewResponse(BaseModel):
    roundName: Optional[str] = None
    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    program: Optional[str] = None
    admissionStatus: Optional[str] = None
    docStatus: Optional[str] = None
    paymentStatus: Optional[str] = None
    academicYear: Optional[str] = None

    class Config:
        from_attributes = True


class ApplicantInformationProblem(BaseModel):
    problemId: Optional[str] = None
    educationId: Optional[str] = None
    applicantId: Optional[str] = None
    details: Optional[str] = None
    updateDate: Optional[str] = None


class AdminRolePageResponse(BaseModel):
    adminId: Optional[str] = None
    prefix: Optional[str] = None 
    firstName: Optional[str] = None 
    lastName: Optional[str] = None 
    email: Optional[str] = None 
    phoneNumber: Optional[str] = None 
    roles: list[str] 
    lastSeen: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class AdminRoleListPageResponse(BaseModel):
    admins: list[AdminRolePageResponse]


class CommitteeResult(BaseModel):
    id: Optional[str]
    shortName: Optional[str]
    name: Optional[str]
    InterviewResult: Optional[str]


class SummaryInterviewPageResponse(BaseModel):
    interviewStatus: Optional[str] = None
    admissionStatus: Optional[str] = None
    docStatus: Optional[str] = None
    paymentStatus: Optional[str] = None
    interviewRoom: Optional[str] = None 
    interviewDate: Optional[str] = None
    interviewTime: Optional[str] = None
    englishScore: Optional[int] = None 
    personalityScore: Optional[int] = None 
    intensionScore: Optional[int] = None 
    computerScore: Optional[int] = None 
    totalScore: Optional[int] = None

    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    fullnameEN: Optional[str] = None
    programRegistered: Optional[str] = None

    program: Optional[str] = None
    roundName: Optional[str] = None

    InterviewCommittee: list[CommitteeResult] = []



class SummaryInterviewListPageResponse(BaseModel):
    applicants: list[SummaryInterviewPageResponse]


class PreEvaUpdateApplicantModel(BaseModel):
    app_id: str
    com_id: str


class EduInterviewEvaResponse(BaseModel):
    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    interviewComId: Optional[str] = None
    prefix: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    interviewRoom: Optional[str] = None
    interviewDate: Optional[str] = None
    interviewTime: Optional[str] = None
    englishScore: Optional[int] = None
    personalityScore: Optional[int] = None
    intensionScore: Optional[int] = None
    computerScore: Optional[int] = None
    totalScore: Optional[int] = None
    englishRemark: Optional[str] = None
    personalityRemark: Optional[str] = None
    intensionRemark: Optional[str] = None
    computerRemark: Optional[str] = None
    totalRemark: Optional[str] = None
    comment: Optional[str] = None
    interviewResult: Optional[str] = None


class EduInterviewEvaListResponse(BaseModel):
    applicants: list[EduInterviewEvaResponse]


class InterviewRoundResponse(BaseModel):
    interviewRoundId: Optional[str] = None
    admissionProgram: Optional[str] = None
    admissionRoundName: Optional[str] = None
    interviewDate: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    duration: Optional[str] = None


class InterviewRoundListResponse(BaseModel):
    interviewRound: list[InterviewRoundResponse]


class InterviewRoundUpdate(BaseModel):
    admissionProgram: Optional[str] = None
    admissionRoundName: Optional[str] = None
    interviewDate: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    duration: Optional[str] = None


class InterviewRoomDetailCreating(BaseModel):
    interviewRoomId: Optional[str] = None
    interviewRoundId: Optional[str] = None
    interviewRoom: Optional[str] = None
    interviewType: Optional[str] = None


class InterviewRoomCommitteeCreating(BaseModel):
    interviewRoomId: Optional[str] = None
    interviewComId: list[str]


class InterviewRoomCommitteeResponse(BaseModel):
    InterviewRoomCommitteeId: Optional[str] = None
    interviewRoomId: Optional[str] = None
    interviewComId: Optional[str] = None


class InterviewCommitteeMember(BaseModel):
    interviewComId: Optional[str] = None
    prefix: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None


class InterviewRoundDetailResponse(BaseModel):
    interviewRoundId: Optional[str] = None
    interviewDate: Optional[str] = None
    interviewStartTime: Optional[str] = None
    interviewEndTime: Optional[str] = None
    admissionProgram: Optional[str] = None
    admissionRoundName: Optional[str] = None

    interviewRoomId: Optional[str] = None
    interviewRoom: Optional[str] = None
    interviewType: Optional[str] = None
    
    interviewComs: list[InterviewCommitteeMember] = []


class InterviewRoundDetailListResponse(BaseModel):
    details: list[InterviewRoundDetailResponse]
    
    
class InterviewRoomCommitteeUpdateRequest(BaseModel):
    interviewRoomId: Optional[str] = None
    interviewComId: Optional[list[str]] = None


class InterviewRoomDetailsResponse(BaseModel):
    interviewRoomId: Optional[str] = None 
    interviewRoom: Optional[str] = None 
    interviewComs: list[InterviewCommitteeMember] = []
    interviewRoundId: Optional[str] = None
    interviewDate: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    duration: Optional[str] = None


class InterviewRoomDetailsListResponse(BaseModel):
    room: list[InterviewRoomDetailsResponse]

class EduApplicantDataViewResponse(BaseModel):
    roundName: Optional[str] = None
    applicantId: Optional[str] = None
    firstnameEN: Optional[str] = None
    lastnameEN: Optional[str] = None
    program: Optional[str] = None
    admissionStatus: Optional[str] = None
    docStatus: Optional[str] = None
    paymentStatus: Optional[str] = None
    academicYear: Optional[str] = None

    class Config:
        from_attributes = True


class ApplicantInformationProblem(BaseModel):
    problemId: Optional[str] = None
    educationId: Optional[str] = None
    applicantId: Optional[str] = None
    details: Optional[str] = None
    updateDate: Optional[str] = None