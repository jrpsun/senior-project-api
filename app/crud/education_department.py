from sqlalchemy.orm import Session
from collections import defaultdict
from typing import Optional

from app.models.course_committee import CourseCommittee
from app.models.education_department import EducationDepartment
from app.models.interview_committee import InterviewCommittee
from app.models.public_relations import PublicRelations
from app.models.interview_round import InterviewRound
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.applicant_contact import ApplicantContact
from app.models.applicant_status import ApplicantStatus
from app.models.admission import Admission
from app.models.preliminary_evaluation import PreliminaryEvaluation
from app.models.interview_evaluation import InterviewEvaluation
from app.models.interview_room_details import InterviewRoomDetails
from app.models.interview_room_committee import InterviewRoomCommittee

from app.schemas.education_department import (
    EducationDepartmentCreate,
    EducationDepartmentUpdate,
    EduApplicantDataMainPageResponse,
    EduListApplicantDataMainPageResponse,
    AdminRolePageResponse,
    AdminRoleListPageResponse,
    SummaryInterviewPageResponse,
    SummaryInterviewListPageResponse,
    PreEvaUpdateApplicantModel,
    EduInterviewEvaResponse,
    EduInterviewEvaListResponse,
    InterviewRoundResponse,
    InterviewRoundListResponse,
    InterviewRoundUpdate,
    InterviewRoomDetailCreating,
    InterviewRoomCommitteeCreating,
    InterviewRoomCommitteeResponse,
    InterviewRoundDetailResponse,
    InterviewRoundDetailListResponse,
    InterviewRoomCommitteeUpdateRequest,
    InterviewRoomDetailsResponse,
    InterviewRoomDetailsListResponse,
    InterviewCommitteeMember
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


def update_courseC_to_applicant(db: Session, assignments: list[PreEvaUpdateApplicantModel]):
    if not assignments:
        raise ValueError("No assignments provided")

    for item in assignments:
        db.query(PreliminaryEvaluation).filter(
            PreliminaryEvaluation.applicantId == item.app_id
        ).update({"courseComId": item.com_id}, synchronize_session=False)

    db.commit()
    return {"message": "Assignments updated successfully"}



# admin manage role page
def get_all_admins_manage_role_page(db: Session):
    # Maps model classes to their unique ID field name
    model_id_map = {
        CourseCommittee: "courseComId",
        EducationDepartment: "educationId",
        InterviewCommittee: "interviewComId",
        PublicRelations: "PRid",
    }

    # Role name for each model
    role_name_map = {
        CourseCommittee: "Course Committee",
        EducationDepartment: "Education Department",
        InterviewCommittee: "Interview Committee",
        PublicRelations: "Public Relations",
    }

    # Dictionary to group unique users by email
    users_map = defaultdict(lambda: {
        "adminId": None,
        "prefix": None,
        "firstName": None,
        "lastName": None,
        "email": None,
        "phoneNumber": None,
        "roles": [],
        "lastSeen": None,
        "username": None,
        "password": None
    })

    # Helper to populate or update a user entry
    def add_user(user, role_name: str, id_field: str):
        if not user or not user.email:
            return
        key = user.email
        user_entry = users_map[key]

        user_entry["adminId"] = getattr(user, id_field, None) or user_entry["adminId"]
        user_entry["prefix"] = getattr(user, "prefix", None) or user_entry["prefix"]
        user_entry["firstName"] = getattr(user, "firstName", None) or user_entry["firstName"]
        user_entry["lastName"] = getattr(user, "lastName", None) or user_entry["lastName"]
        user_entry["email"] = user.email
        user_entry["phoneNumber"] = getattr(user, "phoneNumber", None) or user_entry["phoneNumber"]
        user_entry["lastSeen"] = getattr(user, "lastSeen", None) or user_entry["lastSeen"]
        user_entry["username"] = getattr(user, "username", None) or user_entry["username"]
        user_entry["password"] = getattr(user, "password", None) or user_entry["password"]

        if role_name not in user_entry["roles"]:
            user_entry["roles"].append(role_name)

    # Loop through each model and populate user data
    for model_class in model_id_map:
        role_name = role_name_map[model_class]
        id_field = model_id_map[model_class]
        for user in db.query(model_class).all():
            add_user(user, role_name, id_field)

    # Build final response list
    admin_list = [
        AdminRolePageResponse(**user_data)
        for user_data in users_map.values()
    ]

    return AdminRoleListPageResponse(admins=admin_list)

# interview summary page
def get_all_applicant_summary_interview_page(db: Session):
    query = (
        db.query(
            ApplicantStatus.interviewStatus.label("interviewStatus"),
            ApplicantStatus.admissionStatus.label("admissionStatus"),
            ApplicantStatus.docStatus.label("docStatus"),
            ApplicantStatus.paymentStatus.label("paymentStatus"),
            InterviewEvaluation.interviewRoom.label("interviewRoom"),
            InterviewEvaluation.interviewDate.label("interviewDate"),
            InterviewEvaluation.interviewTime.label("interviewTime"),
            InterviewEvaluation.englishScore.label("englishScore"),
            InterviewEvaluation.personalityScore.label("personalityScore"),
            InterviewEvaluation.intensionScore.label("intensionScore"),
            InterviewEvaluation.computerScore.label("computerScore"),
            InterviewEvaluation.totalScore.label("totalScore"),
            InterviewEvaluation.applicantId.label("applicantId"),
            InterviewEvaluation.interviewComId.label("interviewComId"),
            InterviewEvaluation.interviewResult.label("interviewResult"),
            ApplicantGeneralInformation.firstnameEN.label("firstnameEN"),
            ApplicantGeneralInformation.lastnameEN.label("lastnameEN"),
            ApplicantGeneralInformation.applicantId.label("applicantId_gi"),  # To ensure fallback
            ApplicantGeneralInformation.programRegistered.label("admissionId"),
            Admission.program.label("program"),
            Admission.roundName.label("roundName"),
            InterviewCommittee.prefix.label("cPrefix"),
            InterviewCommittee.firstName.label("cFirstName"),
            InterviewCommittee.lastName.label("cLastName"),
        )
        .select_from(ApplicantGeneralInformation)
        .outerjoin(InterviewEvaluation, InterviewEvaluation.applicantId == ApplicantGeneralInformation.applicantId)
        .outerjoin(InterviewCommittee, InterviewEvaluation.interviewComId == InterviewCommittee.interviewComId)
        .outerjoin(ApplicantStatus, ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId)
        .outerjoin(Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId)
    ).all()

    from collections import defaultdict

    grouped_applicants = defaultdict(lambda: {
        "InterviewCommittee": []
    })

    for row in query:
        applicant_id = row.applicantId or row.applicantId_gi  # fallback in case no interview
        if "interviewStatus" not in grouped_applicants[applicant_id]:
            grouped_applicants[applicant_id].update({
                "interviewStatus": row.interviewStatus,
                "admissionStatus": row.admissionStatus,
                "docStatus": row.docStatus,
                "paymentStatus": row.paymentStatus,
                "interviewRoom": row.interviewRoom,
                "interviewDate": row.interviewDate,
                "interviewTime": row.interviewTime,
                "englishScore": row.englishScore,
                "personalityScore": row.personalityScore,
                "intensionScore": row.intensionScore,
                "computerScore": row.computerScore,
                "totalScore": row.totalScore,
                "applicantId": applicant_id,
                "firstnameEN": row.firstnameEN,
                "lastnameEN": row.lastnameEN,
                "fullnameEN": f"{row.firstnameEN or ''} {row.lastnameEN or ''}".strip(),
                "programRegistered": row.admissionId,
                "program": row.program,
                "roundName": row.roundName,
            })

        if row.interviewComId:
            committee_name = f"{row.cPrefix or ''} {row.cFirstName or ''} {row.cLastName or ''}".strip()
            committee_entry = {
                "id": row.interviewComId,
                "shortName": f"อ. {row.cFirstName or ''}",
                "name": committee_name,
                "InterviewResult": row.interviewResult
            }

            if committee_entry not in grouped_applicants[applicant_id]["InterviewCommittee"]:
                grouped_applicants[applicant_id]["InterviewCommittee"].append(committee_entry)

    response_list = [
        SummaryInterviewPageResponse(**data).model_dump(exclude_unset=True)
        for data in grouped_applicants.values()
    ]

    return SummaryInterviewListPageResponse(applicants=response_list)




def get_all_interview_rooms(db: Session):
    query = (
        db.query(
            InterviewRoomDetails.interviewRoomId.label("interviewRoomId"),
            InterviewRoomDetails.interviewRoom.label("interviewRoom"),
            
            InterviewCommittee.interviewComId.label("interviewComId"),
            InterviewCommittee.prefix.label("prefix"),
            InterviewCommittee.firstName.label("firstName"),
            InterviewCommittee.lastName.label("lastName"),
            
            InterviewRound.interviewRoundId.label("interviewRoundId"),
            InterviewRound.interviewDate.label("interviewDate"),
            InterviewRound.startTime.label("startTime"),
            InterviewRound.endTime.label("endTime"),
            InterviewRound.duration.label("duration"),
        )
        .outerjoin(InterviewRound, InterviewRound.interviewRoundId == InterviewRoomDetails.interviewRoundId)
        .outerjoin(InterviewRoomCommittee, InterviewRoomDetails.interviewRoomId == InterviewRoomCommittee.interviewRoomId)
        .outerjoin(InterviewCommittee, InterviewRoomCommittee.interviewComId == InterviewCommittee.interviewComId)
    ).all()

    grouped_rooms = defaultdict(lambda: {
        "interviewComs": []
    })

    for row in query:
        room_id = row.interviewRoomId
        if "interviewRoom" not in grouped_rooms[room_id]:
            grouped_rooms[room_id].update({
                "interviewRoomId": row.interviewRoomId,
                "interviewRoom": row.interviewRoom,
                "interviewRoundId": row.interviewRoundId,
                "interviewDate": row.interviewDate,
                "startTime": row.startTime,
                "endTime": row.endTime,
                "duration": row.duration,
            })

        if row.interviewComId:
            committee_member = InterviewCommitteeMember(
                interviewComId=row.interviewComId,
                prefix=row.prefix,
                firstName=row.firstName,
                lastName=row.lastName
            )
            if committee_member not in grouped_rooms[room_id]["interviewComs"]:
                grouped_rooms[room_id]["interviewComs"].append(committee_member)

    response_list = [
        InterviewRoomDetailsResponse(**data) for data in grouped_rooms.values()
    ]

    return InterviewRoomDetailsListResponse(room=response_list)


def get_all_applicant_result_interview_eva_page(db: Session, applicant_id: str, committee_id: Optional[str] = None):
    if committee_id:
            query = (
                db.query(
                    InterviewEvaluation.interviewComId.label("interviewComId"),
                    InterviewEvaluation.interviewRoom.label("interviewRoom"),
                    ApplicantGeneralInformation.firstnameTH.label("firstnameTH"),
                    ApplicantGeneralInformation.lastnameTH.label("lastnameTH"),
                    ApplicantGeneralInformation.firstnameEN.label("firstnameEN"),
                    ApplicantGeneralInformation.lastnameEN.label("lastnameEN"),
                    InterviewEvaluation.interviewDate.label("interviewDate"),
                    InterviewEvaluation.interviewTime.label("interviewTime"),
                    InterviewEvaluation.englishScore.label("englishScore"),
                    InterviewEvaluation.personalityScore.label("personalityScore"),
                    InterviewEvaluation.intensionScore.label("intensionScore"),
                    InterviewEvaluation.computerScore.label("computerScore"),
                    InterviewEvaluation.totalScore.label("totalScore"),
                    InterviewEvaluation.englishRemark.label("englishRemark"),
                    InterviewEvaluation.personalityRemark.label("personalityRemark"),
                    InterviewEvaluation.intensionRemark.label("intensionRemark"),
                    InterviewEvaluation.computerRemark.label("computerRemark"),
                    InterviewEvaluation.totalRemark.label("totalRemark"),
                    InterviewEvaluation.comment.label("comment"),
                    InterviewEvaluation.interviewResult.label("interviewResult"),
                    InterviewCommittee.prefix.label("cPrefix"),
                    InterviewCommittee.firstName.label("cFirstName"),
                    InterviewCommittee.lastName.label("cLastName"),
                )
                .filter(InterviewEvaluation.applicantId == applicant_id)
                .filter(InterviewEvaluation.interviewComId == committee_id)
                .outerjoin(InterviewCommittee, InterviewEvaluation.interviewComId == InterviewCommittee.interviewComId)
                .outerjoin(ApplicantGeneralInformation, InterviewEvaluation.applicantId == ApplicantGeneralInformation.applicantId)

        ).all()
    else:
        query = (
            db.query(
                InterviewEvaluation.interviewComId.label("interviewComId"),
                InterviewEvaluation.interviewRoom.label("interviewRoom"),
                ApplicantGeneralInformation.firstnameTH.label("firstnameTH"),
                ApplicantGeneralInformation.lastnameTH.label("lastnameTH"),
                ApplicantGeneralInformation.firstnameEN.label("firstnameEN"),
                ApplicantGeneralInformation.lastnameEN.label("lastnameEN"),
                InterviewEvaluation.interviewDate.label("interviewDate"),
                InterviewEvaluation.interviewTime.label("interviewTime"),
                InterviewEvaluation.englishScore.label("englishScore"),
                InterviewEvaluation.personalityScore.label("personalityScore"),
                InterviewEvaluation.intensionScore.label("intensionScore"),
                InterviewEvaluation.computerScore.label("computerScore"),
                InterviewEvaluation.totalScore.label("totalScore"),
                InterviewEvaluation.englishRemark.label("englishRemark"),
                InterviewEvaluation.personalityRemark.label("personalityRemark"),
                InterviewEvaluation.intensionRemark.label("intensionRemark"),
                InterviewEvaluation.computerRemark.label("computerRemark"),
                InterviewEvaluation.totalRemark.label("totalRemark"),
                InterviewEvaluation.comment.label("comment"),
                InterviewEvaluation.interviewResult.label("interviewResult"),
                InterviewCommittee.prefix.label("cPrefix"),
                InterviewCommittee.firstName.label("cFirstName"),
                InterviewCommittee.lastName.label("cLastName"),
            )
            .filter(InterviewEvaluation.applicantId == applicant_id)
            .outerjoin(InterviewCommittee, InterviewEvaluation.interviewComId == InterviewCommittee.interviewComId)
            .outerjoin(ApplicantGeneralInformation, InterviewEvaluation.applicantId == ApplicantGeneralInformation.applicantId)

        ).all()

    if not query:
        return {"Message": "Applicant not found"}
    
    response_list = []
    for row in query:
        if row.firstnameTH and row.lastnameTH:
            display_firstname = row.firstnameTH
            display_lastname = row.lastnameTH
        else:
            display_firstname = row.firstnameEN
            display_lastname = row.lastnameEN

        response_data = {
            "applicantId": applicant_id,
            "interviewComId": row.interviewComId,
            "prefix": row.cPrefix,
            "firstName": row.cFirstName,
            "lastName": row.cLastName,
            "firstnameEN": display_firstname,
            "lastnameEN": display_lastname,
            "interviewRoom": row.interviewRoom,
            "interviewDate": row.interviewDate,
            "interviewTime": row.interviewTime,
            "englishScore": row.englishScore,
            "personalityScore": row.personalityScore,
            "intensionScore": row.intensionScore,
            "computerScore": row.computerScore,
            "totalScore": row.totalScore,
            "englishRemark": row.englishRemark,
            "personalityRemark": row.personalityRemark,
            "intensionRemark": row.intensionRemark,
            "computerRemark": row.computerRemark,
            "totalRemark": row.totalRemark,
            "comment": row.comment,
            "interviewResult": row.interviewResult,
        }

        response_list.append(EduInterviewEvaResponse(**response_data))


    return EduInterviewEvaListResponse(applicants=response_list)


########## interview round ##########
def get_interview_round(db: Session):
    query = db.query(
        InterviewRound.interviewRoundId.label("interviewRoundId"),
        InterviewRound.admissionProgram.label("admissionProgram"),
        InterviewRound.admissionRoundName.label("admissionRoundName"),
        InterviewRound.interviewDate.label("interviewDate"),
        InterviewRound.startTime.label("startTime"),
        InterviewRound.endTime.label("endTime"),
        InterviewRound.duration.label("duration")
    ).all()

    if not query:
        return {"Message": "Interview Round not found"}

    response_list = []
    for row in query:
        response_data = {
            "interviewRoundId": row.interviewRoundId,
            "admissionProgram": row.admissionProgram,
            "admissionRoundName": row.admissionRoundName,
            "interviewDate": row.interviewDate,
            "startTime": row.startTime, 
            "endTime": row.endTime, 
            "duration": row.duration 
        }

        response_list.append(InterviewRoundResponse(**response_data).model_dump(exclude_unset=True))
    
    return InterviewRoundListResponse(interviewRound=response_list)


def create_interview_round(db: Session, data: InterviewRoundResponse):
    new_interview_round = InterviewRound(
        admissionProgram = data.admissionProgram,
        admissionRoundName = data.admissionRoundName,
        interviewDate = data.interviewDate,
        startTime = data.startTime, 
        endTime = data.endTime, 
        duration = data.duration 
    )
    db.add(new_interview_round)
    db.commit()
    db.refresh(new_interview_round)
    return new_interview_round


def update_interview_round(db: Session, interviewRoundId: str, data: InterviewRoundUpdate):
    db.query(InterviewRound).filter(
        InterviewRound.interviewRoundId == interviewRoundId
    ).update(
        {
            InterviewRound.admissionProgram: data.admissionProgram,
            InterviewRound.admissionRoundName: data.admissionRoundName,
            InterviewRound.interviewDate: data.interviewDate,
            InterviewRound.startTime: data.startTime,
            InterviewRound.endTime: data.endTime,
            InterviewRound.duration: data.duration
        },
        synchronize_session=False
    )

    db.commit()

    return db.query(InterviewRound).filter(InterviewRound.interviewRoundId == interviewRoundId).first()


####################


########## interview room detail ##########
def get_all_interview_room_detail(db: Session):
    return db.query(InterviewRoomDetails).all()


def create_interview_room_detail(db: Session, data: InterviewRoomDetailCreating):
    new_room_detail = InterviewRoomDetails(
        interviewRoomId=data.interviewRoomId,
        interviewRoundId=data.interviewRoundId,
        interviewRoom=data.interviewRoom,
        interviewType=data.interviewType
    )
    db.add(new_room_detail)
    db.commit()
    db.refresh(new_room_detail)
    return new_room_detail


def update_interview_room_detail(db: Session, data: InterviewRoomDetailCreating):
    db.query(InterviewRoomDetails).filter(
        InterviewRoomDetails.interviewRoundId == data.interviewRoundId,
        InterviewRoomDetails.interviewRoomId == data.interviewRoomId
    ).update(
        {
            InterviewRoomDetails.interviewRoom: data.interviewRoom,
            InterviewRoomDetails.interviewType: data.interviewType
        },
        synchronize_session=False
    )

    db.commit()

    return db.query(InterviewRoomDetails).filter(InterviewRoomDetails.interviewRoundId == data.interviewRoundId, InterviewRoomDetails.interviewRoomId == data.interviewRoomId).first()


def delete_interview_room_detail(db: Session, round_id: str, room_id: str):
    delete_room_detail = db.query(InterviewRoomDetails).filter(InterviewRoomDetails.interviewRoundId == round_id, InterviewRoomDetails.interviewRoomId == room_id).first()
    if delete_room_detail:
        db.delete(delete_room_detail)
        db.commit()

    return delete_room_detail


####################


########## interview room committee ##########
def get_all_interview_room_committee(db: Session):
    return db.query(InterviewRoomCommittee).all()


def get_one_interview_room_committee(db: Session, room_id: str):
    return db.query(InterviewRoomCommittee).filter(InterviewRoomCommittee.interviewRoomId == room_id).all()



def create_interview_room_committee(db: Session, data: InterviewRoomCommitteeCreating):
    for com in data.interviewComId:
        new_room_committee = InterviewRoomCommittee(
            interviewRoomId=data.interviewRoomId,
            interviewComId=com
        )
        db.add(new_room_committee)
        db.commit()
        db.refresh(new_room_committee)

    return data

def delete_interview_room_committee(db: Session, interview_room_id: str):
    committees = db.query(InterviewRoomCommittee).filter(
        InterviewRoomCommittee.interviewRoomId == interview_room_id
    ).all()

    if not committees:
        raise HTTPException(status_code=404, detail="No committee records found for the given interview room ID.")

    for committee in committees:
        db.delete(committee)

    db.commit()

    return {"detail": f"Deleted {len(committees)} committee(s) from interview room {interview_room_id}."}



####################


def get_all_interview_room_details(db: Session) -> InterviewRoundDetailListResponse:
    query = db.query(
        InterviewRound.interviewRoundId.label("interviewRoundId"), 
        InterviewRound.interviewDate.label("interviewDate"), 
        InterviewRound.startTime.label("interviewStartTime"), 
        InterviewRound.endTime.label("interviewEndTime"), 
        InterviewRound.admissionProgram.label("admissionProgram"), 
        InterviewRound.admissionRoundName.label("admissionRoundName"), 

        InterviewRoomDetails.interviewRoomId.label("interviewRoomId"), 
        InterviewRoomDetails.interviewRoom.label("interviewRoom"), 
        InterviewRoomDetails.interviewType.label("interviewType"), 

        InterviewRoomCommittee.interviewComId.label("interviewComId"), 
        InterviewCommittee.prefix.label("prefix"), 
        InterviewCommittee.firstName.label("firstName"), 
        InterviewCommittee.lastName.label("lastName")
    ).join(
        InterviewRound, InterviewRoomDetails.interviewRoundId == InterviewRound.interviewRoundId
    ).join(
        InterviewRoomCommittee, InterviewRoomCommittee.interviewRoomId == InterviewRoomDetails.interviewRoomId
    ).join(
        InterviewCommittee, InterviewRoomCommittee.interviewComId == InterviewCommittee.interviewComId
    ).all()

    grouped = defaultdict(lambda: {
        "interviewRoundId": None,
        "interviewDate": None,
        "interviewStartTime": None,
        "interviewEndTime": None,
        "admissionProgram": None,
        "admissionRoundName": None,
        "interviewRoomId": None,
        "interviewRoom": None,
        "interviewType": None,
        "interviewComs": []
    })

    for row in query:
        key = row.interviewRoomId
        group = grouped[key]

        group.update({
            "interviewRoundId": row.interviewRoundId,
            "interviewDate": row.interviewDate,
            "interviewStartTime": row.interviewStartTime,
            "interviewEndTime": row.interviewEndTime,
            "admissionProgram": row.admissionProgram,
            "admissionRoundName": row.admissionRoundName,
            "interviewRoomId": row.interviewRoomId,
            "interviewRoom": row.interviewRoom,
            "interviewType": row.interviewType,
        })

        group["interviewComs"].append({
            "interviewComId": row.interviewComId,
            "prefix": row.prefix,
            "firstName": row.firstName,
            "lastName": row.lastName,
        })

    result = [InterviewRoundDetailResponse(**detail) for detail in grouped.values()]
    return InterviewRoundDetailListResponse(details=result)



    



