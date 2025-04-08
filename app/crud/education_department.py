from sqlalchemy.orm import Session
from collections import defaultdict

from app.models.course_committee import CourseCommittee
from app.models.education_department import EducationDepartment
from app.models.interview_committee import InterviewCommittee
from app.models.public_relations import PublicRelations

from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.applicant_contact import ApplicantContact
from app.models.applicant_status import ApplicantStatus
from app.models.admission import Admission
from app.models.preliminary_evaluation import PreliminaryEvaluation
from app.models.interview_evaluation import InterviewEvaluation

from app.schemas.education_department import (
    EducationDepartmentCreate,
    EducationDepartmentUpdate,
    EduApplicantDataMainPageResponse,
    EduListApplicantDataMainPageResponse,
    AdminRolePageResponse,
    AdminRoleListPageResponse,
    SummaryInterviewPageResponse,
    SummaryInterviewListPageResponse
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

# edu screening page
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

        firstname = (
            general.firstnameTH if general.firstnameTH and general.firstnameTH.lower() != "string"
            else general.firstnameEN
        )
        lastname = (
            general.lastnameTH if general.lastnameTH and general.lastnameTH.lower() != "string"
            else general.lastnameEN
        )

        response_data["firstnameEN"] = firstname
        response_data["lastnameEN"] = lastname

        if general:
            response_data.update({
                k: v for k, v in general.__dict__.items()
                if k not in ["firstnameTH", "lastnameTH", "firstnameEN", "lastnameEN"]
            })

        if contact:
            response_data.update(contact.__dict__)

        if status:
            response_data.update(status.__dict__)

        if admit:
            response_data.update(admit.__dict__)

        response_list.append(EduApplicantDataMainPageResponse(**response_data).model_dump(exclude_unset=True))


    return EduListApplicantDataMainPageResponse(applicants=response_list)


def update_courseC_to_applicant(db: Session, app_id: list[str], com_id: list[str]):
    # Ensure the number of applicants is divisible by the number of courses (com_ids)
    if len(app_id) % len(com_id) != 0:
        raise ValueError("The number of applicants must be divisible by the number of com_ids")

    # Determine how many applicants should be assigned to each com_id
    num_applicants_per_com = len(app_id) // len(com_id)

    for i, com in enumerate(com_id):
        # Get the subset of app_ids to assign the current com_id
        start_idx = i * num_applicants_per_com
        end_idx = (i + 1) * num_applicants_per_com
        app_ids_for_com = app_id[start_idx:end_idx]

        # Update the courseComId for each applicant in the subset
        for app in app_ids_for_com:
            db.query(PreliminaryEvaluation).filter(PreliminaryEvaluation.applicantId == app).update({"courseComId": com}, synchronize_session=False)

    db.commit()

    return {"message": "Course assignments updated successfully"}



def get_all_admins_manage_role_page(db: Session):
    # Store unique users using their email as identifier
    users_map = defaultdict(lambda: {
        "roles": [],
        "prefix": None,
        "firstName": None,
        "lastName": None,
        "email": None,
        "phoneNumber": None,
        "lastSeen": None
    })

    # Helper to add or update user
    def add_user(user, role_name: str):
        if not user or not user.email:
            return
        key = user.email
        user_entry = users_map[key]

        # Populate basic info (first time only, or overwrite if needed)
        user_entry["prefix"] = getattr(user, "prefix", None) or user_entry["prefix"]
        user_entry["firstName"] = getattr(user, "firstName", None) or user_entry["firstName"]
        user_entry["lastName"] = getattr(user, "lastName", None) or user_entry["lastName"]
        user_entry["email"] = user.email
        user_entry["phoneNumber"] = getattr(user, "phoneNumber", None) or user_entry["phoneNumber"]
        user_entry["lastSeen"] = getattr(user, "lastSeen", None) or user_entry["lastSeen"]

        # Add role if not already added
        if role_name not in user_entry["roles"]:
            user_entry["roles"].append(role_name)

    # Fetch from each role table
    for user in db.query(CourseCommittee).all():
        add_user(user, "Course Committee")

    for user in db.query(EducationDepartment).all():
        add_user(user, "Education Department")

    for user in db.query(InterviewCommittee).all():
        add_user(user, "Interview Committee")

    for user in db.query(PublicRelations).all():
        add_user(user, "Public Relations")

    # Transform dict to response model
    admin_list = [
        AdminRolePageResponse(**user_data)
        for user_data in users_map.values()
    ]

    return AdminRoleListPageResponse(admins=admin_list)


def get_all_applicant_summary_interview_page(db: Session):
    query = (
        db.query(
            ApplicantStatus.interviewStatus.label("interviewStatus"),
            InterviewEvaluation.interviewRoom.label("interviewRoom"),
            InterviewEvaluation.englishScore.label("englishScore"),
            InterviewEvaluation.personalityScore.label("personalityScore"),
            InterviewEvaluation.intensionScore.label("intensionScore"),
            InterviewEvaluation.computerScore.label("computerScore"),
            InterviewEvaluation.totalScore.label("totalScore"),
            InterviewEvaluation.applicantId.label("applicantId"),
            InterviewEvaluation.interviewComId.label("interviewComId"),
            ApplicantGeneralInformation.firstnameEN.label("firstnameEN"),
            ApplicantGeneralInformation.lastnameEN.label("lastnameEN"),
            ApplicantGeneralInformation.programRegistered.label("admissionId"),
            Admission.program.label("program"),
            Admission.roundName.label("roundName"),
            InterviewCommittee.prefix.label("cPrefix"),
            InterviewCommittee.firstName.label("cFirstName")
        )
        .outerjoin(ApplicantGeneralInformation, InterviewEvaluation.applicantId == ApplicantGeneralInformation.applicantId)
        .outerjoin(InterviewCommittee, InterviewEvaluation.interviewComId == InterviewCommittee.interviewComId)
        .outerjoin(Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId)
        .outerjoin(ApplicantStatus, ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId)
    ).all()

    if not query:
        return {"Message": "Applicant not found"}

    grouped_applicants = defaultdict(lambda: {
        "InterviewCommittee": []
    })

    for row in query:
        applicant_id = row.applicantId
        if "interviewStatus" not in grouped_applicants[applicant_id]:
            grouped_applicants[applicant_id].update({
                "interviewStatus": row.interviewStatus,
                "interviewRoom": row.interviewRoom,
                "englishScore": row.englishScore,
                "personalityScore": row.personalityScore,
                "intensionScore": row.intensionScore,
                "computerScore": row.computerScore,
                "totalScore": row.totalScore,
                "applicantId": row.applicantId,
                "firstnameEN": row.firstnameEN,
                "lastnameEN": row.lastnameEN,
                "programRegistered": row.admissionId,
                "program": row.program,
                "roundName": row.roundName,
            })

        # Add each committee member's name to the list
        committee_name = f"{row.cPrefix or ''} {row.cFirstName or ''}".strip()
        if committee_name and committee_name not in grouped_applicants[applicant_id]["InterviewCommittee"]:
            grouped_applicants[applicant_id]["InterviewCommittee"].append(committee_name)

    # Build the final response
    response_list = []
    for data in grouped_applicants.values():
        response_list.append(SummaryInterviewPageResponse(**data).model_dump(exclude_unset=True))

    return SummaryInterviewListPageResponse(applicants=response_list)



