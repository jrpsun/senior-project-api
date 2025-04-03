from sqlalchemy.orm import Session
from app.models.education_department import EducationDepartment
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.applicant_contact import ApplicantContact
from app.models.applicant_status import ApplicantStatus
from app.models.admission import Admission
from app.models.preliminary_evaluation import PreliminaryEvaluation
from app.schemas.education_department import (
    EducationDepartmentCreate,
    EducationDepartmentUpdate,
    EduApplicantDataMainPageResponse,
    EduListApplicantDataMainPageResponse
)
from datetime import datetime


def create_education_department(db: Session, edu_data: EducationDepartmentCreate):
    new_edu = EducationDepartment(
        educationId=edu_data.educationId,
        prefix=edu_data.prefix,
        firstName=edu_data.firstName,
        lastName=edu_data.lastName,
        username=edu_data.username,
        password=edu_data.password,
        email=edu_data.email,
        phoneNumber=edu_data.phoneNumber,
        lastSeen=datetime.now().strftime("%d-%m-%Y %H.%M")
    )
    db.add(new_edu)
    db.commit()
    db.refresh(new_edu)
    return new_edu


def get_all_education_departments(db: Session):
    return db.query(EducationDepartment).all()


def get_education_department(db: Session, edu_id: str):
    return db.query(EducationDepartment).filter(EducationDepartment.educationId == edu_id).first()


def update_education_department(db: Session, edu_id: str, edu_data: EducationDepartmentUpdate):
    edu_record = db.query(EducationDepartment).filter(EducationDepartment.educationId == edu_id).first()
    if not edu_record:
        return None
    
    for key, value in edu_data.model_dump(exclude_unset=True).items():
        setattr(edu_record, key, value)

    db.commit()
    db.refresh(edu_record)
    return edu_record


def delete_education_department(db: Session, edu_id: str):
    edu_record = db.query(EducationDepartment).filter(EducationDepartment.educationId == edu_id).first()
    if edu_record:
        db.delete(edu_record)
        db.commit()
    return edu_record


def get_all_applicants_edu_main_page(db: Session):
    query = (
        db.query(
            ApplicantGeneralInformation,
            ApplicantContact,
            ApplicantStatus,
            Admission
        )
        .outerjoin(ApplicantContact, ApplicantGeneralInformation.applicantId == ApplicantContact.applicantId)
        .outerjoin(ApplicantStatus, ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId)
        .outerjoin(Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId)
    ).all()

    print(query)
    if not query:
        return {"Message": "Applicant not found"}
    
    response_list = []
    for general, contact, status, admit in query:
        response_data = {}

        if general:
            response_data.update(general.__dict__)

        if contact:
            response_data.update(contact.__dict__)

        if status:
            response_data.update(status.__dict__)

        if admit:
            response_data.update(admit.__dict__)

        response_list.append(EduApplicantDataMainPageResponse(**response_data).model_dump(exclude_unset=True))

    return EduListApplicantDataMainPageResponse(applicants=response_list)


def update_courseC_to_applicant(db: Session, app_id: list[str], com_id: list[str]):
    for i in range(len(app_id)):
        update_preEva = db.query(PreliminaryEvaluation).filter(PreliminaryEvaluation.applicantId == app_id[i]).update({"courseComId": com_id[i]}, synchronize_session=False)
    
    db.commit()
    
    return update_preEva
