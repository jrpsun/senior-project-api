from sqlalchemy.orm import Session
from app.models.course_committee import CourseCommittee
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.preliminary_evaluation import PreliminaryEvaluation
from app.models.applicant_status import ApplicantStatus
from app.models.admission import Admission
from app.schemas.course_committee import (
    CourseCommitteeCreate,
    CourseCommitteeUpdate,
    CourseApplicantDataMainPageResponse,
    CourseListApplicantDataMainPageResponse,
    PreEvaPageResponse
)
from datetime import datetime


def create_course_committee(db: Session, committee_data: CourseCommitteeCreate):
    new_committee = CourseCommittee(
        courseComId=committee_data.courseComId,
        prefix=committee_data.prefix,
        firstName=committee_data.firstName,
        lastName=committee_data.lastName,
        username=committee_data.username,
        password=committee_data.password,
        email=committee_data.email,
        phoneNumber=committee_data.phoneNumber,
        lastSeen=datetime.now().strftime("%d-%m-%Y %H.%M")
    )
    db.add(new_committee)
    db.commit()
    db.refresh(new_committee)
    return new_committee


def get_all_course_committees(db: Session):
    return db.query(CourseCommittee).all()


def get_course_committee(db: Session, committee_id: str):
    return db.query(CourseCommittee).filter(CourseCommittee.courseComId == committee_id).first()


def update_course_committee(db: Session, committee_id: str, committee_data: CourseCommitteeUpdate):
    committee_record = db.query(CourseCommittee).filter(CourseCommittee.courseComId == committee_id).first()
    if not committee_record:
        return None
    
    for key, value in committee_data.model_dump(exclude_unset=True).items():
        setattr(committee_record, key, value)

    db.commit()
    db.refresh(committee_record)
    return committee_record


def delete_course_committee(db: Session, committee_id: str):
    committee_record = db.query(CourseCommittee).filter(CourseCommittee.courseComId == committee_id).first()
    if committee_record:
        db.delete(committee_record)
        db.commit()
    return committee_record


def get_all_applicants_course_main_page(db: Session):
    query = (
        db.query(
            PreliminaryEvaluation.applicantId.label("applicantId"),
            PreliminaryEvaluation.preEvaDate.label("preEvaDate"),
            CourseCommittee.prefix.label("courseC_prefix"),
            CourseCommittee.firstName.label("courseC_firstName"),
            CourseCommittee.lastName.label("courseC_lastName"),
            ApplicantStatus.admissionStatus.label("admissionStatus"),
            ApplicantStatus.docStatus.label("docStatus"),
            Admission.roundName.label("roundName"),
            Admission.program.label("program"),
            ApplicantGeneralInformation.firstnameEN.label("firstnameEN"),
            ApplicantGeneralInformation.lastnameEN.label("lastnameEN")
        )
        .outerjoin(CourseCommittee, PreliminaryEvaluation.courseComId == CourseCommittee.courseComId)
        .outerjoin(ApplicantGeneralInformation, PreliminaryEvaluation.applicantId == ApplicantGeneralInformation.applicantId)
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
            "prefix": row.courseC_prefix,
            "firstName": row.courseC_firstName,
            "lastName": row.courseC_lastName,
            "preEvaDate": row.preEvaDate
        }

        response_list.append(CourseApplicantDataMainPageResponse(**response_data).model_dump(exclude_unset=True))

    return CourseListApplicantDataMainPageResponse(applicants=response_list)


def get_pre_eva_page(db :Session, applicant_id: str):
    query = (
        db.query(
            PreliminaryEvaluation.applicantId.label("applicantId"),
            PreliminaryEvaluation.preEvaDate.label("preEvaDate"),
            PreliminaryEvaluation.preliminaryEva.label("preliminaryEva"),
            PreliminaryEvaluation.preliminaryComment.label("preliminaryComment"),
            CourseCommittee.prefix.label("courseC_prefix"),
            CourseCommittee.firstName.label("courseC_firstName"),
            CourseCommittee.lastName.label("courseC_lastName"),
            ApplicantGeneralInformation.firstnameEN.label("firstnameEN"),
            ApplicantGeneralInformation.lastnameEN.label("lastnameEN")
            )
            .outerjoin(CourseCommittee, PreliminaryEvaluation.courseComId == CourseCommittee.courseComId)
            .outerjoin(ApplicantGeneralInformation, PreliminaryEvaluation.applicantId == ApplicantGeneralInformation.applicantId)
            .filter(PreliminaryEvaluation.applicantId == applicant_id)
    )

    if not query:
        return {"Message": "Applicant not found"}
    
    for row in query:
        response_data = {

        "applicantId": row.applicantId,
        "firstnameEN": row.firstnameEN,
        "lastnameEN": row.lastnameEN,
        "comPrefix": row.courseC_prefix,
        "firstName": row.courseC_firstName,
        "lastName": row.courseC_lastName,
        "preEvaDate": row.preEvaDate,
        "preliminaryEva": row.preliminaryEva,
        "preliminaryComment": row.preliminaryComment

        }

        PreEvaPageResponse(**response_data).model_dump(exclude_unset=True)

    return response_data


def update_pre_eva_to_applicant(db: Session, app_id: str, com_id: str, preEvaResult: str, comment: str):
    
    update_pre_Eva = db.query(PreliminaryEvaluation).filter(
        PreliminaryEvaluation.applicantId == app_id,
        PreliminaryEvaluation.courseComId == com_id
        ).update(
        {

            "preliminaryEva": preEvaResult,
            "preliminaryComment": comment

        }, synchronize_session=False
        )
    
    db.commit()
    
    return update_pre_Eva