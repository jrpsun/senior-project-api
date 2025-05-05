import uuid
from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from collections import defaultdict
from typing import Optional, List, Dict
from sqlalchemy import and_
from app.models import *
from datetime import datetime
from app.schemas.education_department import *


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

def model_to_dict(obj):
    if obj is None:
        return None
    obj_dict = obj.__dict__.copy()
    obj_dict.pop('_sa_instance_state', None)
    return obj_dict
# edu screening page
def get_all_applicants_edu_main_page(db: Session):
    query = (
        db.query(
            ApplicantGeneralInformation,
            ApplicantContact,
            ApplicantStatus,
            ApplicantAdmissionCancel,
            Admission,
            ApplicantRegistrations
        )
        .outerjoin(
            ApplicantContact,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantContact.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantContact.programRegistered
            )
        )
        .outerjoin(
            ApplicantStatus,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantStatus.programRegistered
            )
        )
        .outerjoin(
            ApplicantAdmissionCancel,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantAdmissionCancel.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantAdmissionCancel.programRegistered
            )
        )
        .outerjoin(Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId)
        .outerjoin(ApplicantRegistrations, ApplicantGeneralInformation.applicantId == ApplicantRegistrations.applicantId)
    ).all()
    result = []
    for general, contact, status, cancel, admit, register in query:
        data = {
            "roundName": admit.roundName if admit.roundName else None,
            "applicantId": register.applicantId,
            "applicantNumber": general.applicant_number,
            "admissionId": admit.admissionId,
            "firstnameEN": register.firstnameTH if register.firstnameTH not in [None, ""] else register.firstnameEN,
            "lastnameEN": register.lastnameTH if register.lastnameTH not in [None, ""] else register.lastnameEN,
            "program": admit.program if admit.program else None,
            "year": admit.academicYear if admit.academicYear else None,
            "admissionStatus": status.admissionStatus if status.admissionStatus else None,
            "docStatus": status.docStatus if status.docStatus else None,
            "paymentStatus": status.paymentStatus if status.paymentStatus else None,
            "applicantEmail": register.applicantEmail if register.applicantEmail else None,
            "applicantPhone": contact.applicantPhone if contact.applicantPhone else None,
            "reason": cancel.reason if cancel else None,
            "moreDetail": cancel.moreDetail if cancel else None
        }
        result.append(data)

    return result


def update_courseC_to_applicant(db: Session, assignments: list[PreEvaUpdateApplicantModel]):
    if not assignments:
        raise ValueError("No assignments provided")

    for item in assignments:
        db.query(PreliminaryEvaluation).filter(
            PreliminaryEvaluation.applicantId == item.app_id
        ).update({"courseComId": item.com_id}, synchronize_session=False)

        db.query(ApplicantStatus).filter(
            ApplicantStatus.applicantId == item.app_id
        ).update({"admissionStatus": "03 - รอพิจารณา"}, synchronize_session=False)

    db.commit()
    return {"message": "Assignments updated successfully"}

def get_applicant_edu_main_page_by_id(app_id: str, admId: str, db: Session):
    query = (
        db.query(
            ApplicantGeneralInformation,
            ApplicantContact,
            ApplicantStatus,
            Admission,
            ApplicantRegistrations
        )
        .outerjoin(
            ApplicantContact,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantContact.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantContact.programRegistered
            )
        )
        .outerjoin(
            ApplicantStatus,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantStatus.programRegistered
            )
        )
        .outerjoin(Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId)
        .outerjoin(ApplicantRegistrations, ApplicantGeneralInformation.applicantId == ApplicantRegistrations.applicantId)
        .filter(ApplicantGeneralInformation.applicantId == app_id)
        .first()
    )

    if not query:
        return {"message": "Applicant not found"}

    general, contact, status, admit, regis = query
    response_data = {}

    if general:
        response_data.update(general.__dict__)

    if contact:
        response_data.update(contact.__dict__)

    if status:
        response_data.update(status.__dict__)

    if admit:
        response_data.update(admit.__dict__)

    if regis:
        response_data.update(regis.__dict__)

    return EduApplicantDataViewResponse(**response_data).model_dump(exclude_unset=True)




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
        CourseCommittee: "กรรมการหลักสูตร",
        EducationDepartment: "เจ้าหน้าที่งานการศึกษา",
        InterviewCommittee: "กรรมการสัมภาษณ์",
        PublicRelations: "ประชาสัมพันธ์ (PR)",
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
            ApplicantGeneralInformation.firstnameTH.label("firstnameTH"),
            ApplicantGeneralInformation.lastnameTH.label("lastnameTH"),
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
        firstname = row.firstnameTH if row.firstnameTH and row.firstnameTH.lower() != "string" else row.firstnameEN
        lastname = row.lastnameTH if row.lastnameTH and row.lastnameTH.lower() != "string" else row.lastnameEN

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
                "firstnameEN": firstname,
                "lastnameEN": lastname,
                "fullnameEN": f"{firstname} {lastname}".strip(),
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
                    InterviewEvaluation.educationId.label("educationId"),
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
                    InterviewEvaluation.evaDate.label("evaDate"),
                    InterviewEvaluation.outstandingLevel.label("outstandingLevel"),

                    InterviewCommittee.prefix.label("cPrefix"),
                    InterviewCommittee.firstName.label("cFirstName"),
                    InterviewCommittee.lastName.label("cLastName"),

                    EducationDepartment.firstName.label("educationName")
                )
                .filter(InterviewEvaluation.applicantId == applicant_id)
                .filter(InterviewEvaluation.interviewComId == committee_id)
                .outerjoin(InterviewCommittee, InterviewEvaluation.interviewComId == InterviewCommittee.interviewComId)
                .outerjoin(EducationDepartment, InterviewEvaluation.educationId == EducationDepartment.educationId)
                .outerjoin(ApplicantGeneralInformation, InterviewEvaluation.applicantId == ApplicantGeneralInformation.applicantId)
        
        ).all()
    else:
        query = (
            db.query(
            InterviewEvaluation.interviewComId.label("interviewComId"),
            InterviewEvaluation.interviewRoom.label("interviewRoom"),
            InterviewEvaluation.educationId.label("educationId"),

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
            InterviewEvaluation.evaDate.label("evaDate"),
            InterviewEvaluation.outstandingLevel.label("outstandingLevel"),

            InterviewCommittee.prefix.label("cPrefix"),
            InterviewCommittee.firstName.label("cFirstName"),
            InterviewCommittee.lastName.label("cLastName"),

            EducationDepartment.firstName.label("educationName")
            )
            .filter(InterviewEvaluation.applicantId == applicant_id)
            .outerjoin(InterviewCommittee, InterviewEvaluation.interviewComId == InterviewCommittee.interviewComId)
            .outerjoin(EducationDepartment, InterviewEvaluation.educationId == EducationDepartment.educationId)
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
            "educationId": row.educationId,
            "evaDate": row.evaDate,
            "educationName": row.educationName,
            "outstandingLevel": row.outstandingLevel
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



def create_or_updated_applicant_problem(db: Session, app_id: str, edu_id: str, admId: str, data: str):
    if data == "เอกสารครบถ้วน":
        (db.query(ApplicantStatus)
         .filter(ApplicantStatus.applicantId == app_id)
         .filter(ApplicantStatus.programRegistered == admId)
         .update(
            {"docStatus": "03 - เอกสารครบถ้วน"}
        ))
    else:
        (db.query(ApplicantStatus)
         .filter(ApplicantStatus.applicantId == app_id)
         .filter(ApplicantStatus.programRegistered == admId)
         .update(
            {"docStatus": "04 - เอกสารไม่ครบถ้วน"}
        ))
    db.commit()

    applicant = (db.query(InformationProblem)
                 .filter(InformationProblem.applicantId == app_id)
                 .filter(InformationProblem.programRegistered == admId)
                 .first()
                )

    if applicant:
        applicant.details = data

        db.commit()
        db.refresh(applicant)

        return { "message": f"Updated applicant problem with id {app_id} success"}
    
    applicant = InformationProblem(
        problemId = uuid.uuid4(),
        educationId = edu_id,
        applicantId = app_id,
        programRegistered = admId,
        details = data,
        updateDate = datetime.today().strftime('%Y-%m-%d %H:%M')
    )

    db.add(applicant)
    db.commit()
    db.refresh(applicant)

    return { "message": f"Created applicant problem with id {app_id} success"}


def get_applicant_information_problem(db: Session, app_id: str, admId):
    problems = (db.query(InformationProblem)
                .filter(InformationProblem.applicantId == app_id)
                .filter(InformationProblem.programRegistered == admId)
                .first()
            )
    
    if not problems:
        raise HTTPException(status_code=404, detail=f"Applicant with ID: {app_id} not found")
    
    return problems


def create_interview_eva_final(db: Session, final_data: FinalInterviewResult):
    adStatus = "07 - ผ่านการสอบสัมภาษณ์" if final_data.interviewResult == "pass" else "08 - ไม่ผ่านการสอบสัมภาษณ์"
    intStatus = "04 - ผ่านการสัมภาษณ์" if final_data.interviewResult == "pass" else "05 - ไม่ผ่านการสัมภาษณ์"

    new_eva = InterviewEvaluation(
        applicantId=final_data.applicantId,
        educationId=final_data.educationId,
        comment=final_data.comment,
        evaDate=final_data.evaDate
    )
    

    applicant_status_updated = db.query(ApplicantStatus).filter(
        ApplicantStatus.applicantId == final_data.applicantId
    ).update(
        {
            ApplicantStatus.admissionStatus: adStatus,
            ApplicantStatus.interviewStatus: intStatus
        },
        synchronize_session=False
    )

    db.add(new_eva)
    db.commit()
    db.refresh(new_eva)

    return new_eva and applicant_status_updated


def get_int_eva_edu_result(db: Session, app_id: str, edu_id: str):
    query = (
        db.query(
            InterviewEvaluation.applicantId.label("applicantId"),
            InterviewEvaluation.educationId.label("educationId"),
            InterviewEvaluation.comment.label("comment"),
            InterviewEvaluation.evaDate.label("evaDate"),
            EducationDepartment.firstName.label("firstName")
        )
        .filter(InterviewEvaluation.applicantId == app_id, InterviewEvaluation.educationId == edu_id)
        .outerjoin(EducationDepartment, InterviewEvaluation.educationId == EducationDepartment.educationId)
    )

    if not query:
        return {"Message": "Applicant or Education not found"}

    for row in query:
        response_data = {
            "applicantId": row.applicantId,
            "educationId": row.educationId,
            "comment": row.comment,
            "evaDate": row.evaDate,
            "firstName": row.firstName
        }

        InterviewEvaEduResult(**response_data).model_dump(exclude_unset=True)

    return response_data



def get_pre_eva_summary(db: Session):
    query = (
        db.query(
            PreliminaryEvaluation.courseComId.label("courseComId"),
            PreliminaryEvaluation.preliminaryEva.label("preliminaryEva"),
            PreliminaryEvaluation.preliminaryComment.label("preliminaryComment"),
            ApplicantGeneralInformation.applicantId.label("applicantId"),
            ApplicantGeneralInformation.firstnameTH.label("firstnameTH"),
            ApplicantGeneralInformation.lastnameTH.label("lastnameTH"),
            ApplicantGeneralInformation.firstnameEN.label("firstnameEN"),
            ApplicantGeneralInformation.lastnameEN.label("lastnameEN"),
            ApplicantGeneralInformation.programRegistered.label("programRegistered"),
            Admission.program.label("program"),
            Admission.roundName.label("roundName"),
            CourseCommittee.prefix.label("prefix"),
            CourseCommittee.firstName.label("cFirstName"),
            CourseCommittee.lastName.label("cLastName"),
        )
        .join(ApplicantGeneralInformation, PreliminaryEvaluation.applicantId == ApplicantGeneralInformation.applicantId)
        .join(CourseCommittee, PreliminaryEvaluation.courseComId == CourseCommittee.courseComId)
        .join(Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId)
    ).all()

    # Group by courseComId (committee)
    grouped: Dict[str, Dict] = defaultdict(lambda: {
        "courseComId": None,
        "prefix": "",
        "firstname": "",
        "lastName": "",
        "applicants": [],
        "passed": 0,
        "failed": 0,
        "pending": 0
    })

    for row in query:
        # Name fallback logic
        firstname = row.firstnameTH if row.firstnameTH and row.firstnameTH.lower() != "string" else row.firstnameEN
        lastname = row.lastnameTH if row.lastnameTH and row.lastnameTH.lower() != "string" else row.lastnameEN

        # Prepare applicant data
        applicant_data = {
            "applicantId": row.applicantId,
            "firstnameEN": firstname,
            "lastnameEN": lastname,
            "preliminaryEva": row.preliminaryEva,
            "preliminaryComment": row.preliminaryComment,
            "programRegistered": row.programRegistered,
            "program": row.program,
            "roundName": row.roundName,
        }

        group = grouped[row.courseComId]

        # Only set committee info once
        if group["courseComId"] is None:
            group["courseComId"] = row.courseComId
            group["prefix"] = row.prefix
            group["firstName"] = row.cFirstName
            group["lastName"] = row.cLastName

        # Count passed/failed/pending
        if row.preliminaryEva == "ผ่านการคัดกรอง":
            group["passed"] += 1
        elif row.preliminaryEva == "ไม่ผ่านการคัดกรอง":
            group["failed"] += 1
        else:
            group["pending"] += 1

        # Add applicant
        group["applicants"].append(applicant_data)

    # Convert to list
    response_list = [
        PreEvaSummaryResponse(
            courseComId=data["courseComId"],
            prefix=data["prefix"],
            firstName=data["firstName"],
            lastName=data["lastName"],
            applicants=[
                PreEvaSummaryApplicantsResponse(**applicant) for applicant in data["applicants"]
            ],
            passed=data["passed"],
            failed=data["failed"],
            pending=data["pending"]
        )
        for data in grouped.values()
    ]

    return PreEvaSummaryListResponse(preEva=response_list)


def get_interview_summary(db: Session) -> IntEvaSummaryListResponse:
    rooms = db.query(InterviewRoomDetails).all()
    
    response_list = []

    for room in rooms:
        # Find interview round
        interview_round = db.query(InterviewRound).filter(InterviewRound.interviewRoundId == room.interviewRoundId).first()

        # Find committees in the room
        committees = (
            db.query(InterviewCommittee)
            .join(InterviewRoomCommittee, InterviewCommittee.interviewComId == InterviewRoomCommittee.interviewComId)
            .filter(InterviewRoomCommittee.interviewRoomId == room.interviewRoomId)
            .all()
        )

        committee_names = [f"อ. {c.firstName}" for c in committees]
        combined_committee_name = ", ".join(committee_names)

        # Find all applicants evaluated in the room
        evaluations = (
            db.query(InterviewEvaluation)
            .filter(
                InterviewEvaluation.interviewRoom == room.interviewRoom,
                InterviewEvaluation.educationId == None
            )
            .all()
        )

        # Group evaluations by applicant
        applicant_evaluations = {}
        for eva in evaluations:
            if eva.applicantId not in applicant_evaluations:
                applicant_evaluations[eva.applicantId] = []
            applicant_evaluations[eva.applicantId].append(eva)

        applicants_list = []

        for applicant_id, evals in applicant_evaluations.items():
            # Average all scores
            english_avg = sum([e.englishScore or 0 for e in evals]) / len(evals)
            personality_avg = sum([e.personalityScore or 0 for e in evals]) / len(evals)
            intention_avg = sum([e.intensionScore or 0 for e in evals]) / len(evals)
            computer_avg = sum([e.computerScore or 0 for e in evals]) / len(evals)
            total_avg = sum([e.totalScore or 0 for e in evals]) / len(evals)

            # Get applicant info
            applicant_info = db.query(ApplicantGeneralInformation).filter(ApplicantGeneralInformation.applicantId == applicant_id).first()

            if applicant_info:
                firstname = applicant_info.firstnameTH or applicant_info.firstnameEN or ""
                lastname = applicant_info.lastnameTH or applicant_info.lastnameEN or ""
            else:
                firstname = ""
                lastname = ""

            # Get interview status
            status = db.query(ApplicantStatus).filter(ApplicantStatus.applicantId == applicant_id).first()
            interview_status = status.interviewStatus if status else None

            # Pick interviewResult: most common one among evaluations
            interview_results = [e.interviewResult for e in evals if e.interviewResult is not None]
            interview_result = max(set(interview_results), key=interview_results.count) if interview_results else None

            applicants_list.append(
                IntEvaSummaryApplicantsResponse(
                    applicantId=applicant_id,
                    firstnameEN=firstname,
                    lastnameEN=lastname,
                    interviewRoom=room.interviewRoom,
                    englishScore=round(english_avg, 2),
                    personalityScore=round(personality_avg, 2),
                    intentionScore=round(intention_avg, 2),
                    computerScore=round(computer_avg, 2),
                    totalScore=round(total_avg, 2),
                    #InterviewCommitteeId=None,  # optional, can set if needed
                    interviewResult=interview_result,
                    interviewStatus=interview_status
                )
            )

        response_list.append(
            IntEvaSummaryResponse(
                committee=combined_committee_name,
                interviewRoom=room.interviewRoom,
                admissionProgram=interview_round.admissionProgram if interview_round else None,
                admissionRoundName=interview_round.admissionRoundName if interview_round else None,
                applicants=applicants_list
            )
        )

    return IntEvaSummaryListResponse(intEva=response_list)


def get_all_int_slot(db: Session) -> list[AllIntEvaResponse]:
    # Query only the needed fields and filter out None values
    result = db.query(
        InterviewEvaluation.interviewRoundId,
        InterviewEvaluation.interviewRoom,
        InterviewEvaluation.interviewTime
    ).filter(
        InterviewEvaluation.educationId == None,
        InterviewEvaluation.interviewRoundId != None,
        InterviewEvaluation.interviewRoom != None,
        InterviewEvaluation.interviewTime != None,
    ).all()

    # Group by (interviewRoundId, interviewRoom)
    grouped = defaultdict(set)
    for round_id, room, time in result:
        grouped[(round_id, room)].add(time)

    # Convert to list of schema objects
    response = [
        AllIntEvaResponse(
            interviewRoundId=round_id,
            interviewRoom=room,
            interviewTime=sorted(list(times))  # sort optional
        )
        for (round_id, room), times in grouped.items()
    ]

    return response
