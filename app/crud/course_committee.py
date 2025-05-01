from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from typing import Optional
from app.models.applicant_registrations import ApplicantRegistrations
from app.models.course_committee import CourseCommittee
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.preliminary_evaluation import PreliminaryEvaluation
from app.models.applicant_status import ApplicantStatus
from app.models.admission import Admission
from app.models.applicant_status import ApplicantStatus
from app.schemas.course_committee import (
    CourseCommitteeCreate,
    CourseCommitteeUpdate,
    CourseApplicantDataMainPageResponse,
    CourseListApplicantDataMainPageResponse,
    PreEvaPageResponse,
    PreEvaRequest
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
    query = db.query(CourseCommittee).all()

    if not query:
        raise HTTPException(status_code=404, detail="Course Committee not found")
    
    return query


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

# course com screening page
def get_all_applicants_course_main_page(db: Session, committee_id: Optional[str] = None):
    query = db.query(
            PreliminaryEvaluation.applicantId.label("applicantId"),
            PreliminaryEvaluation.preEvaDate.label("preEvaDate"),
            PreliminaryEvaluation.preliminaryEva.label("preliminaryEva"),
            PreliminaryEvaluation.preliminaryComment.label("preliminaryComment"),
            CourseCommittee.courseComId.label("courseComId"),
            CourseCommittee.prefix.label("courseC_prefix"),
            CourseCommittee.firstName.label("courseC_firstName"),
            CourseCommittee.lastName.label("courseC_lastName"),
            ApplicantStatus.admissionStatus.label("admissionStatus"),
            ApplicantStatus.docStatus.label("docStatus"),
            ApplicantStatus.paymentStatus.label("paymentStatus"),
            Admission.roundName.label("roundName"),
            Admission.program.label("program"),
            ApplicantRegistrations.firstnameEN.label("firstnameEN"),
            ApplicantRegistrations.lastnameEN.label("lastnameEN"),
            ApplicantRegistrations.firstnameTH.label("firstnameTH"),
            ApplicantRegistrations.lastnameTH.label("lastnameTH"),
            ApplicantGeneralInformation.applicant_number.label("applicantNumber"),
        )
    
    if committee_id:
        query = query.filter(PreliminaryEvaluation.courseComId == committee_id)

    query = query.outerjoin(CourseCommittee, PreliminaryEvaluation.courseComId == CourseCommittee.courseComId)
    query = query.outerjoin(
        ApplicantStatus,
        and_(
            PreliminaryEvaluation.applicantId == ApplicantStatus.applicantId,
            PreliminaryEvaluation.programRegistered == ApplicantStatus.programRegistered
        )
    )
    query = query.outerjoin(ApplicantRegistrations, PreliminaryEvaluation.applicantId == ApplicantRegistrations.applicantId)
    query = query.outerjoin(Admission, PreliminaryEvaluation.programRegistered == Admission.admissionId)
    query = query.outerjoin(
        ApplicantGeneralInformation,
        and_(
            PreliminaryEvaluation.applicantId == ApplicantGeneralInformation.applicantId,
            PreliminaryEvaluation.programRegistered == ApplicantGeneralInformation.programRegistered
        )
    )
    
    
    result = query.all()

    if not result:
        return {"Message": "Applicant not found"}
    
    response_list = []
    for row in result:
        firstname = row.firstnameTH if row.firstnameTH and row.firstnameTH.lower() != "string" else row.firstnameEN
        lastname = row.lastnameTH if row.lastnameTH and row.lastnameTH.lower() != "string" else row.lastnameEN

        response_data = {
            "roundName": row.roundName,
            "applicantId": row.applicantId,
            "firstnameEN": firstname,
            "lastnameEN": lastname,
            "fullnameEN": f"{firstname} {lastname}",
            "program": row.program,
            "admissionStatus": row.admissionStatus,
            "docStatus": row.docStatus,
            "paymentStatus": row.paymentStatus,
            "courseComId": row.courseComId,
            "prefix": row.courseC_prefix,
            "firstName": row.courseC_firstName,
            "lastName": row.courseC_lastName,
            "preEvaDate": row.preEvaDate,
            "preliminaryEva": row.preliminaryEva,
            "preliminaryComment": row.preliminaryComment,
            "applicantNumber": row.applicantNumber
        }

        response_list.append(CourseApplicantDataMainPageResponse(**response_data).model_dump(exclude_unset=True))

    return CourseListApplicantDataMainPageResponse(applicants=response_list)



# pre eva tab in view applicant information page
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


# Pre Eva Page
def update_pre_eva_to_applicant(db: Session, payload: PreEvaRequest):
    status = "04 - ผ่านการพิจารณา" if payload.preEvaResult == "ผ่านการคัดกรอง" else "05 - ไม่ผ่านการพิจารณา"

    pre_eva_updated = db.query(PreliminaryEvaluation).filter(
        PreliminaryEvaluation.applicantId == payload.app_id,
        PreliminaryEvaluation.courseComId == payload.com_id
    ).update(
        {
            PreliminaryEvaluation.preliminaryEva: payload.preEvaResult,
            PreliminaryEvaluation.preliminaryComment: payload.comment,
            PreliminaryEvaluation.preEvaDate: payload.preEvaDate
        },
        synchronize_session=False
    )

    applicant_status_updated = db.query(ApplicantStatus).filter(
        ApplicantStatus.applicantId == payload.app_id
    ).update(
        {
            ApplicantStatus.admissionStatus: status
        },
        synchronize_session=False
    )

    db.commit()

    return pre_eva_updated and applicant_status_updated