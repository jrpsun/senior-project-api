from sqlalchemy.orm import Session
from app.models.interview_committee import InterviewCommittee
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.interview_evaluation import InterviewEvaluation
from app.models.applicant_status import ApplicantStatus
from app.models.admission import Admission
from app.models.interview_round import InterviewRound
from app.models.interview_room_details import InterviewRoomDetails
from app.models.interview_room_committee import InterviewRoomCommittee
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
    InterviewEvaUpdate
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

# interview com screening page
def get_all_applicants_interview_main_page(db: Session, committee_id: str):
    subquery = (
        db.query(
            InterviewEvaluation.applicantId.label("applicantId"),
            InterviewEvaluation.interviewDate.label("interviewDate"),
            InterviewEvaluation.interviewTime.label("interviewTime"),
            InterviewEvaluation.interviewRoom.label("interviewRoom"),
            InterviewEvaluation.interviewComId.label("interviewComId"),
            InterviewCommittee.prefix.label("prefix"),
            InterviewCommittee.firstName.label("firstName"),
            InterviewCommittee.lastName.label("lastName"),
        )
        .join(InterviewCommittee, InterviewEvaluation.interviewComId == InterviewCommittee.interviewComId)
        .subquery()
    )

    query = (
        db.query(
            subquery.c.applicantId,
            subquery.c.interviewDate,
            subquery.c.interviewTime,
            subquery.c.interviewRoom,
            subquery.c.interviewComId,
            subquery.c.prefix,
            subquery.c.firstName,
            subquery.c.lastName,
            ApplicantGeneralInformation.firstnameEN,
            ApplicantGeneralInformation.lastnameEN,
            ApplicantGeneralInformation.firstnameTH,
            ApplicantGeneralInformation.lastnameTH,
            ApplicantStatus.admissionStatus,
            ApplicantStatus.docStatus,
            ApplicantStatus.interviewStatus,
            Admission.roundName,
            Admission.program
        )
        .outerjoin(ApplicantGeneralInformation, subquery.c.applicantId == ApplicantGeneralInformation.applicantId)
        .outerjoin(Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId)
        .outerjoin(ApplicantStatus, ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId)
    ).all()

    if not query:
        return {"Message": "Applicant not found"}

    # Group by applicantId to collect both committee members
    applicant_map = {}
    for row in query:
        app_id = row.applicantId

        firstname = row.firstnameTH if row.firstnameTH and row.firstnameTH.lower() != "string" else row.firstnameEN
        lastname = row.lastnameTH if row.lastnameTH and row.lastnameTH.lower() != "string" else row.lastnameEN

        if app_id not in applicant_map:
            applicant_map[app_id] = {
                "roundName": row.roundName,
                "applicantId": app_id,
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
            # Add second committee
            applicant_map[app_id]["prefix2"] = row.prefix
            applicant_map[app_id]["firstName2"] = row.firstName
            applicant_map[app_id]["lastName2"] = row.lastName

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
def update_interview_eva_to_applicant(db: Session, app_id: str, com_id: str, inEva_data: InterviewEvaUpdate):
    db.query(InterviewEvaluation).filter(
        InterviewEvaluation.applicantId == app_id,
        InterviewEvaluation.interviewComId == com_id
    ).update(
        {
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
            "interviewResult": inEva_data.interviewResult
        }, synchronize_session=False
    )

    evaluations = db.query(InterviewEvaluation).filter(
        InterviewEvaluation.applicantId == app_id
    ).all()

    results = [eva.interviewResult for eva in evaluations]

    results = [res for res in results if res is not None]

    if len(results) == 2:
        if all(res == "ผ่านการสัมภาษณ์" for res in results):
            interviewStatus = "04 - ผ่านการสัมภาษณ์"
        elif all(res == "ไม่ผ่านการสัมภาษณ์" for res in results):
            interviewStatus = "05 - ไม่ผ่านการสัมภาษณ์"
        elif set(results) == {"ผ่านการสัมภาษณ์", "ไม่ผ่านการสัมภาษณ์"}:
            interviewStatus = "03 - รอพิจารณาเพิ่มเติม"
        else:
            interviewStatus = "02 - ไม่มาสัมภาษณ์"
    elif len(results) == 1:
        interviewStatus = "06 - รอผลการประเมินเพิ่มเติม"
    else:
        interviewStatus = "02 - ไม่มาสัมภาษณ์"

    db.query(ApplicantStatus).filter(
        ApplicantStatus.applicantId == app_id
    ).update(
        {"interviewStatus": interviewStatus}, synchronize_session=False
    )

    if interviewStatus == "04 - ผ่านการสัมภาษณ์":
        admissionStatus = "07 - ผ่านการสัมภาษณ์"
    elif interviewStatus == "05 - ไม่ผ่านการสัมภาษณ์":
        admissionStatus = "08 - ไม่ผ่านการสัมภาษณ์"
    elif interviewStatus == "03 - รอพิจารณาเพิ่มเติม":
        admissionStatus = "06 - รอสัมภาษณ์"
    elif interviewStatus == "06 - รอผลการประเมินเพิ่มเติม":
        admissionStatus = "06 - รอสัมภาษณ์"    
    else:
        admissionStatus = "08 - ไม่ผ่านการสัมภาษณ์"

    db.query(ApplicantStatus).filter(
        ApplicantStatus.applicantId == app_id
    ).update(
        {"admissionStatus": admissionStatus}, synchronize_session=False
    )


    db.commit()

    return True


def create_interview_eva(db: Session, newEva_data: list[InterviewEvaCreate]):
    new_evaluations = []
    
    for eva in newEva_data:
        for committee_id in eva.committeeId:  
            new_eva = InterviewEvaluation(
                applicantId = eva.applicantId,
                interviewComId = committee_id,
                interviewDate = eva.intDate,
                interviewTime = eva.intTime,
                interviewRoom = eva.room
            )
            db.add(new_eva)
            new_evaluations.append(new_eva)

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

