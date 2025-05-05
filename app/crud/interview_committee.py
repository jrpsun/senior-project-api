from sqlalchemy.orm import Session
from app.models.interview_committee import InterviewCommittee
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.interview_evaluation import InterviewEvaluation
from app.models.applicant_status import ApplicantStatus
from app.models.admission import Admission
from app.models.interview_round import InterviewRound
from app.models.interview_room_details import InterviewRoomDetails
from app.models.interview_room_committee import InterviewRoomCommittee
from app.models.applicant_registrations import ApplicantRegistrations
from sqlalchemy import and_
from app.schemas.interview_committee import (
    InterviewCommitteeCreate,
    InterviewCommitteeUpdate,
    InterviewApplicantDataMainPageResponse,
    InterviewListApplicantDataMainPageResponse,
    InterviewEvaPageResponse,
    InterviewEvaListPageResponse,
    InterviewEvaCreate,
    InterviewRoundCreate,
    InterviewRoomCreate,
    InterviewRoomUpdate,
    InterviewEvaUpdate,
    EditInterviewRoom
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
        lastSeen=datetime.now().strftime("%Y-%m-%d %H:%M")
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

# interview com screening page
def get_all_applicants_interview_main_page(db: Session, committee_id: str):
    # Step 1: Get only applicantId and programRegistered pairs for this committee
    filtered_eval_subquery = (
        db.query(
            InterviewEvaluation.applicantId,
            InterviewEvaluation.programRegistered
        )
        .filter(InterviewEvaluation.interviewComId == committee_id)
        .distinct()
        .subquery()
    )

    # Step 2: Get full evaluation info for only the filtered (applicantId, programRegistered)
    subquery = (
        db.query(
            InterviewEvaluation.applicantId.label("applicantId"),
            InterviewEvaluation.programRegistered.label("admissionId"),
            InterviewEvaluation.interviewDate.label("interviewDate"),
            InterviewEvaluation.interviewTime.label("interviewTime"),
            InterviewEvaluation.interviewRoom.label("interviewRoom"),
            InterviewEvaluation.interviewComId.label("interviewComId"),
            InterviewCommittee.prefix.label("prefix"),
            InterviewCommittee.firstName.label("firstName"),
            InterviewCommittee.lastName.label("lastName"),
        )
        .join(InterviewCommittee, InterviewEvaluation.interviewComId == InterviewCommittee.interviewComId)
        .join(filtered_eval_subquery, and_(
            InterviewEvaluation.applicantId == filtered_eval_subquery.c.applicantId,
            InterviewEvaluation.programRegistered == filtered_eval_subquery.c.programRegistered
        ))
        .subquery()
    )

    # Step 3: Join other related tables using the applicantId + admissionId
    query = (
        db.query(
            subquery.c.applicantId,
            subquery.c.admissionId,
            subquery.c.interviewDate,
            subquery.c.interviewTime,
            subquery.c.interviewRoom,
            subquery.c.interviewComId,
            subquery.c.prefix,
            subquery.c.firstName,
            subquery.c.lastName,
            ApplicantRegistrations.firstnameEN,
            ApplicantRegistrations.lastnameEN,
            ApplicantRegistrations.firstnameTH,
            ApplicantRegistrations.lastnameTH,
            ApplicantStatus.admissionStatus,
            ApplicantStatus.docStatus,
            ApplicantStatus.interviewStatus,
            Admission.admissionId,
            Admission.roundName,
            Admission.program
        )
        .outerjoin(
            ApplicantGeneralInformation,
            and_(
                subquery.c.applicantId == ApplicantGeneralInformation.applicantId,
                subquery.c.admissionId == ApplicantGeneralInformation.programRegistered
            )
        )
        .outerjoin(ApplicantRegistrations, ApplicantGeneralInformation.applicantId == ApplicantRegistrations.applicantId)
        .outerjoin(Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId)
        .outerjoin(
            ApplicantStatus,
            and_(
                subquery.c.applicantId == ApplicantStatus.applicantId,
                subquery.c.admissionId == ApplicantStatus.programRegistered
            )
        )
        .all()
    )

    if not query:
        return {"applicants": []}

    # Step 4: Group by applicantId + admissionId
    applicant_map = {}
    for row in query:
        key = (row.applicantId, row.admissionId)

        firstname = row.firstnameTH if row.firstnameTH and row.firstnameTH.lower() != 'none' else row.firstnameEN
        lastname = row.lastnameTH if row.lastnameTH and row.lastnameTH.lower() != 'none' else row.lastnameEN

        if key not in applicant_map:
            applicant_map[key] = {
                "admissionId": row.admissionId,
                "roundName": row.roundName,
                "applicantId": row.applicantId,
                "firstnameEN": firstname,
                "lastnameEN": lastname,
                "program": row.program,
                "admissionStatus": row.admissionStatus,
                "docStatus": row.docStatus,
                "interviewStatus": row.interviewStatus,
                "interviewRoom": row.interviewRoom,
                "interviewDate": row.interviewDate,
                "interviewTime": row.interviewTime,
                "prefix1": row.prefix,
                "firstName1": row.firstName,
                "lastName1": row.lastName,
                "prefix2": None,
                "firstName2": None,
                "lastName2": None
            }
        else:
            if not applicant_map[key]["prefix2"]:
                applicant_map[key]["prefix2"] = row.prefix
                applicant_map[key]["firstName2"] = row.firstName
                applicant_map[key]["lastName2"] = row.lastName

    response_list = [
        InterviewApplicantDataMainPageResponse(**data).model_dump(exclude_unset=True)
        for data in applicant_map.values()
    ]

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
            "englishRemark" : row.englishRemark,  
            "personalityRemark" : row.personalityRemark,
            "intensionRemark" : row.intensionRemark,
            "computerRemark" : row.computerRemark,
            "totalRemark" : row.totalRemark,
            "comment": row.comment

        }

        response_list.append(InterviewEvaPageResponse(**response_data).model_dump(exclude_unset=True))

    return InterviewEvaListPageResponse(applicants=response_list)

# interview eva page
def update_interview_eva_to_applicant(db: Session, app_id: str, com_id: str, adm_id: str, inEva_data: InterviewEvaUpdate):
    update_data = {
        "englishScore": inEva_data.englishScore,
        "personalityScore": inEva_data.personalityScore,
        "intensionScore": inEva_data.intensionScore, 
        "computerScore": inEva_data.computerScore,
        "totalScore": inEva_data.totalScore,
        "comment": inEva_data.comment,
        "englishRemark": inEva_data.englishRemark,
        "personalityRemark": inEva_data.personalityRemark,
        "intensionRemark": inEva_data.intensionRemark,
        "computerRemark": inEva_data.computerRemark,
        "totalRemark": inEva_data.totalRemark,
        "outstandingLevel": inEva_data.outstandingLevel
    }

    if inEva_data.interviewResult is not None:
        update_data["interviewResult"] = inEva_data.interviewResult

    db.query(InterviewEvaluation).filter(
        InterviewEvaluation.applicantId == app_id,
        InterviewEvaluation.programRegistered == adm_id,
        InterviewEvaluation.interviewComId == com_id
    ).update(update_data, synchronize_session=False)

    # Get all evaluations
    evaluations = db.query(InterviewEvaluation).filter(
        InterviewEvaluation.applicantId == app_id,
        InterviewEvaluation.programRegistered == adm_id,
        InterviewEvaluation.educationId == None
    ).all()


    results = [eva.interviewResult for eva in evaluations]

    # Separate logic-friendly sets
    all_results_set = set(results)
    non_null_results = [r for r in results if r is not None]
    unique_non_null_set = set(non_null_results)

    # Priority-based decision tree
    if "ไม่มาสัมภาษณ์" in all_results_set:
        interviewStatus = "02 - ไม่มาสัมภาษณ์"
        admissionStatus = "08 - ไม่ผ่านการสอบสัมภาษณ์"

    elif "รอพิจารณาเพิ่มเติม" in all_results_set:
        interviewStatus = "03 - รอพิจารณาเพิ่มเติม"
        admissionStatus = "06 - รอสัมภาษณ์"

    elif len(non_null_results) < len(results):
        interviewStatus = "06 - รอผลการประเมิน"
        admissionStatus = "06 - รอสัมภาษณ์"

    else:
        if unique_non_null_set == {"ผ่านการสัมภาษณ์"}:
            interviewStatus = "04 - ผ่านการสัมภาษณ์"
            admissionStatus = "07 - ผ่านการสอบสัมภาษณ์"
        elif unique_non_null_set == {"ไม่ผ่านการสัมภาษณ์"}:
            interviewStatus = "05 - ไม่ผ่านการสัมภาษณ์"
            admissionStatus = "08 - ไม่ผ่านการสอบสัมภาษณ์"
        elif unique_non_null_set == {"ผ่านการสัมภาษณ์", "ไม่ผ่านการสัมภาษณ์"}:
            interviewStatus = "03 - รอพิจารณาเพิ่มเติม"
            admissionStatus = "06 - รอสัมภาษณ์"
        else:
            interviewStatus = "02 - ไม่มาสัมภาษณ์"
            admissionStatus = "08 - ไม่ผ่านการสอบสัมภาษณ์"

    # Save statuses
    db.query(ApplicantStatus).filter(
        ApplicantStatus.applicantId == app_id,
        ApplicantStatus.programRegistered == adm_id
    ).update({"interviewStatus": interviewStatus}, synchronize_session=False)

    db.query(ApplicantStatus).filter(
        ApplicantStatus.applicantId == app_id,
        ApplicantStatus.programRegistered == adm_id
    ).update({"admissionStatus": admissionStatus}, synchronize_session=False)

    db.commit()
    return True






def create_interview_eva(db: Session, newEva_data: list[InterviewEvaCreate]):
    new_evaluations = []

    for eva in newEva_data:
        for committee_id in eva.committeeId:
            new_eva = InterviewEvaluation(
                applicantId=eva.applicantId,
                programRegistered=eva.programRegistered,
                interviewComId=committee_id,
                interviewRoundId=eva.interviewRoundId,
                interviewRoom=eva.room,
                interviewDate=eva.intDate,
                interviewTime=eva.intTime,
            )
            db.add(new_eva)
            new_evaluations.append(new_eva)

        db.query(ApplicantStatus).filter(
            ApplicantStatus.applicantId == eva.applicantId, 
            ApplicantStatus.programRegistered == eva.programRegistered
        ).update({
            "admissionStatus": "06 - รอสัมภาษณ์",
            "interviewStatus": "01 - รอสัมภาษณ์"
        }, synchronize_session=False)
        

    db.commit()
    for e in new_evaluations:
        db.refresh(e)

    return new_evaluations



def create_interview_round(db: Session, newEvaRound_data: InterviewRoundCreate):
    new_evaluation_round = []

    new_eva_round = InterviewRound(
        admissionProgram = newEvaRound_data.admissionProgram,
        admissionRoundName = newEvaRound_data.admissionRoundName,
        interviewDate = newEvaRound_data.interviewDate,
        startTime = newEvaRound_data.startTime,
        endTime = newEvaRound_data.endTime,
        duration = newEvaRound_data.duration
    )
    db.add(new_eva_round)
    new_evaluation_round.append(new_eva_round)

    db.commit()
    
    return new_evaluation_round


def update_interview_round(db: Session, round_id: str, EvaRound_data: InterviewRoundCreate):
    
    update_int_round = db.query(InterviewRound).filter(InterviewRound.interviewRoundId == round_id).update(
        {
            "admissionProgram": EvaRound_data.admissionProgram,
            "admissionRoundName": EvaRound_data.admissionRoundName,
            "interviewDate": EvaRound_data.interviewDate,
            "startTime": EvaRound_data.startTime, 
            "endTime": EvaRound_data.endTime, 
            "duration": EvaRound_data.duration, 

        }, synchronize_session=False
        )
    
    db.commit()
    
    return update_int_round


def create_interview_room(db: Session, newIntRoom_data: InterviewRoomCreate):

    new_int_room = InterviewRoomDetails(
        interviewRoundId = newIntRoom_data.interviewRoundId,
        interviewRoom = newIntRoom_data.interviewRoom,
        interviewType = newIntRoom_data.interviewType,
    )

    db.add(new_int_room)
    db.commit()  
    db.refresh(new_int_room)  
    

    for com_id in newIntRoom_data.interviewComId:
        new_room_committee = InterviewRoomCommittee(
            interviewRoomId = new_int_room.interviewRoomId,
            interviewComId = com_id
        )
        db.add(new_room_committee)

    db.commit()  

    return new_int_room


def update_interview_room(db: Session, room_id: str, IntRoom_data: InterviewRoomUpdate):
    
    db.query(InterviewRoomDetails).filter(InterviewRoomDetails.interviewRoomId == room_id).update(
        {
            "interviewRoom": IntRoom_data.interviewRoom,
            "interviewType": IntRoom_data.interviewType
        }, synchronize_session=False
    )

    if IntRoom_data.interviewRoundId:
        db.query(InterviewRound).filter(InterviewRound.interviewRoundId == IntRoom_data.interviewRoundId).update(
            {
                "interviewDate": IntRoom_data.interviewDate,
                "startTime": IntRoom_data.startTime, 
                "endTime": IntRoom_data.endTime, 
                "duration": IntRoom_data.duration
            }, synchronize_session=False
        )

    db.query(InterviewRoomCommittee).filter(InterviewRoomCommittee.interviewRoomId == room_id).delete(synchronize_session=False)

    for com_id in IntRoom_data.interviewComId:
        new_committee = InterviewRoomCommittee(
            interviewRoomId=room_id,
            interviewComId=com_id
        )
        db.add(new_committee)

    db.commit()
    
    return {"message": "Interview Room updated successfully"}


# updating interview room for interview auto grouping page
def update_interview_room_auto_group(db: Session, update_data: EditInterviewRoom):
    db.query(InterviewEvaluation).filter(
        InterviewEvaluation.applicantId == update_data.applicantId,
        InterviewEvaluation.programRegistered == update_data.programRegistered
        ).update(
        {
            InterviewEvaluation.interviewRoundId: update_data.interviewRoundId,
            InterviewEvaluation.interviewRoom: update_data.interviewRoom,
            InterviewEvaluation.interviewTime: update_data.interviewTime
        },
        synchronize_session=False
    )

    db.commit()

    return db.query(InterviewEvaluation).filter(InterviewEvaluation.applicantId == update_data.applicantId).all()

