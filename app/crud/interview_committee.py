from sqlalchemy.orm import Session
from app.models.interview_committee import InterviewCommittee
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.interview_evaluation import InterviewEvaluation
from app.models.applicant_status import ApplicantStatus
from app.models.admission import Admission
from app.schemas.interview_committee import (
    InterviewCommitteeCreate,
    InterviewCommitteeUpdate,
    InterviewApplicantDataMainPageResponse,
    InterviewListApplicantDataMainPageResponse,
    InterviewEvaPageResponse,
    InterviewEvaListPageResponse
)
from datetime import datetime


def create_interview_committee(db: Session, ic_data: InterviewCommitteeCreate):
    new_ic = InterviewCommittee(
        interviewComId=ic_data.interviewComId,
        prefix=ic_data.prefix,
        firstName=ic_data.firstName,
        lastName=ic_data.lastName,
        username=ic_data.username,
        password=ic_data.password,
        email=ic_data.email,
        phoneNumber=ic_data.phoneNumber,
        lastSeen=datetime.now().strftime("%d-%m-%Y %H.%M")
    )
    db.add(new_ic)
    db.commit()
    db.refresh(new_ic)
    return new_ic


def get_interview_committees(db: Session):
    return db.query(InterviewCommittee).all()


def get_interview_committee_by_id(db: Session, ic_id: str):
    return db.query(InterviewCommittee).filter(InterviewCommittee.interviewComId == ic_id).first()


def update_interview_committee(db: Session, ic_id: str, ic_data: InterviewCommitteeUpdate):
    ic_record = db.query(InterviewCommittee).filter(InterviewCommittee.interviewComId == ic_id).first()
    if not ic_record:
        return None

    for key, value in ic_data.model_dump(exclude_unset=True).items():
        setattr(ic_record, key, value)

    db.commit()
    db.refresh(ic_record)
    return ic_record


def delete_interview_committee(db: Session, ic_id: str):
    ic_record = db.query(InterviewCommittee).filter(InterviewCommittee.interviewComId == ic_id).first()
    if ic_record:
        db.delete(ic_record)
        db.commit()
    return ic_record


def get_all_applicants_interview_main_page(db: Session):
    query = (
        db.query(
            InterviewEvaluation.applicantId.label("applicantId"),
            InterviewEvaluation.interviewDate.label("interviewDate"),
            InterviewEvaluation.interviewTime.label("interviewTime"),
            InterviewEvaluation.interviewRoom.label("interviewRoom"),
            InterviewCommittee.prefix.label("interviewC_prefix"),
            InterviewCommittee.firstName.label("interviewC_firstName"),
            InterviewCommittee.lastName.label("interviewC_lastName"),
            ApplicantStatus.admissionStatus.label("admissionStatus"),
            ApplicantStatus.docStatus.label("docStatus"),
            Admission.roundName.label("roundName"),
            Admission.program.label("program"),
            ApplicantGeneralInformation.firstnameEN.label("firstnameEN"),
            ApplicantGeneralInformation.lastnameEN.label("lastnameEN"),

        )
        .outerjoin(InterviewCommittee, InterviewEvaluation.interviewComId == InterviewCommittee.interviewComId)
        .outerjoin(ApplicantGeneralInformation, InterviewEvaluation.applicantId == ApplicantGeneralInformation.applicantId)
        .outerjoin(Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId)
        .outerjoin(ApplicantStatus, ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId)
    ).all()

    if not query:
        return {"Message": "Applicant not found"}
    
    response_list = []
    for row in query:
        response_data = {
            "roundName": row.roundName,
            "applicantId": row.applicantId,
            "firstnameEN": row.firstnameEN,
            "lastnameEN": row.lastnameEN,
            "program": row.program,
            "admissionStatus": row.admissionStatus,
            "docStatus": row.docStatus,
            "interviewRoom": row.interviewRoom,
            "prefix": row.interviewC_prefix,
            "firstName": row.interviewC_firstName,
            "lastName": row.interviewC_lastName,
            "interviewDate": row.interviewDate,
            "interviewTime": row.interviewTime
        }

        response_list.append(InterviewApplicantDataMainPageResponse(**response_data).model_dump(exclude_unset=True))

    return InterviewListApplicantDataMainPageResponse(applicants=response_list)


def get_interview_eva_page(db :Session, applicant_id: str):
    query = (
        db.query(
            InterviewEvaluation.applicantId.label("applicantId"),
            InterviewEvaluation.englishScore.label("englishScore"),
            InterviewEvaluation.personalityScore.label("personalityScore"),
            InterviewEvaluation.intensionScore.label("intensionScore"),
            InterviewEvaluation.computerScore.label("computerScore"),
            InterviewEvaluation.totalScore.label("totalScore"),
            InterviewEvaluation.comment.label("comment"),
            InterviewEvaluation.interviewDate.label("interviewDate"),
            InterviewEvaluation.interviewTime.label("interviewTime"),
            InterviewEvaluation.interviewResult.label("interviewResult"),
            InterviewEvaluation.englishRemark.label("englishRemark"),  
            InterviewEvaluation.personalityRemark.label("personalityRemark"),
            InterviewEvaluation.intensionRemark.label("intensionRemark"),
            InterviewEvaluation.computerRemark.label("computerRemark"),
            InterviewEvaluation.totalRemark.label("totalRemark"),
            InterviewCommittee.prefix.label("interviewC_prefix"),
            InterviewCommittee.firstName.label("interviewC_firstName"),
            ApplicantGeneralInformation.firstnameEN.label("firstnameEN"),
            ApplicantGeneralInformation.lastnameEN.label("lastnameEN"),
            ApplicantStatus.admissionStatus.label("admissionStatus")
            )
            .outerjoin(InterviewCommittee, InterviewEvaluation.interviewComId == InterviewCommittee.interviewComId)
            .outerjoin(ApplicantStatus, InterviewEvaluation.applicantId == ApplicantStatus.applicantId)
            .outerjoin(ApplicantGeneralInformation, PreliminaryEvaluation.applicantId == ApplicantGeneralInformation.applicantId)
            .filter(InterviewEvaluation.applicantId == applicant_id)
    )

    if not query:
        return {"Message": "Applicant not found"}
    
    response_list = []
    for row in query:
        response_data = {

            "applicantId": row.applicantId,
            "firstnameEN": row.firstnameEN,
            "lastnameEN": row.lastnameEN,
            "admissionStatus": row.admissionStatus,
            "comPrefix": row.interviewC_prefix,
            "firstName": row.interviewC_firstName,
            "interviewDate": row.interviewDate,
            "interviewTime": row.interviewTime,
            "interviewResult": row.interviewResult,
            "englishScore": row.englishScore,
            "personalityScore": row.personalityScore,
            "intensionScore": row.intensionScore,
            "computerScore": row.computerScore,
            "totalScore": row.totalScore,
            "interviewRemark": row.interviewRemark,
            "englishRemark" : row.englishRemark,  
            "personalityRemark" : row.personalityRemark,
            "intensionRemark" : row.intensionRemark,
            "computerRemark" : row.computerRemark,
            "totalRemark" : row.totalRemark,
            "comment": row.comment

        }

        response_list.append(PreEvaPageResponse(**response_data).model_dump(exclude_unset=True))

    return InterviewEvaListPageResponse(applicants=response_list)


def update_interview_eva_to_applicant(
    db: Session, app_id: str, com_id: str, e_score: int, p_score: int, i_score: int, c_score: int, t_score: int, comment: str,
    result: str, er: str, pr: str, ir: str, cr: str, tr: str
    ): # TODO: add result: str, remark: str
    
    update_interview_Eva = db.query(InterviewEvaluation).filter(
        InterviewEvaluation.applicantId == app_id,
        InterviewEvaluation.interviewComId == com_id
        ).update(
        {

            "englishScore": e_score,
            "PersonalityScore": p_score,
            "intersionScore": i_score,
            "computerScore": c_score,
            "totalScore": t_score,
            "comment": comment
           # "interviewResult": result,
           # "interviewRemark": remark

        }, synchronize_session=False
        )
    
    db.commit()
    
    return update_interview_Eva