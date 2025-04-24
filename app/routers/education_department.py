from typing import Optional
from app.schemas.education_department import *
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import education_department as crud

router = APIRouter()


@router.post("/", response_model=EducationDepartmentResponse)
def create_edu_dep(edu_data: EducationDepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_education_department(db, edu_data)


@router.get("/get-edu/{edu_id}", response_model=EducationDepartmentResponse)
def read_edu_dep(edu_id: str, db: Session = Depends(get_db)):
    edu_dep = crud.get_education_department(db, edu_id)
    if not edu_dep:
        raise HTTPException(status_code=404, detail="Education Department not found")
    return edu_dep


@router.get("/get-all-edu", response_model=list[EducationDepartmentResponse])
def read_all_edu_deps(db: Session = Depends(get_db)):
    return crud.get_all_education_departments(db)


@router.put("/update-edu/{edu_id}", response_model=EducationDepartmentResponse)
def update_edu_dep(edu_id: str, edu_data: EducationDepartmentUpdate, db: Session = Depends(get_db)):
    updated_edu_dep = crud.update_education_department(db, edu_id, edu_data)
    if not updated_edu_dep:
        raise HTTPException(status_code=404, detail="Education Department not found2")
    return updated_edu_dep


@router.delete("/delete-edu/{edu_id}")
def delete_edu_dep(edu_id: str, db: Session = Depends(get_db)):
    deleted_edu_dep = crud.delete_education_department(db, edu_id)
    if not deleted_edu_dep:
        raise HTTPException(status_code=404, detail="Education Department not found")
    return {"message": "Education Department deleted successfully"}


@router.get("/all-applicant-edu", response_model=EduListApplicantDataMainPageResponse)
def read_all_applicants(db: Session = Depends(get_db)):
    read_all_applicants = crud.get_all_applicants_edu_main_page(db)
    if not read_all_applicants:
        raise HTTPException(status_code=404, detail="Applicant Information not found")
    return read_all_applicants


@router.get("/applicant-edu/{app_id}", response_model=EduApplicantDataViewResponse)
def get_applicant(app_id: str, db: Session = Depends(get_db)):
    applicant = crud.get_applicant_edu_main_page_by_id(app_id, db)
    if not applicant:
        raise HTTPException(status_code=404, detail=f"Applicant Information with id {app_id} not found")
    return applicant


@router.put("/update-edu-preEva")
def update_edu_preEva(assignments: list[PreEvaUpdateApplicantModel], db: Session = Depends(get_db)):
    edu_update_preEva = crud.update_courseC_to_applicant(db, assignments)
    if not edu_update_preEva:
        raise HTTPException(status_code=404, detail="Education Department not found")
    return edu_update_preEva


@router.get("/get-all-admins", response_model=AdminRoleListPageResponse)
def get_all_admins(db: Session = Depends(get_db)):
    get_all_admins = crud.get_all_admins_manage_role_page(db)
    if not get_all_admins:
        raise HTTPException(status_code=404, detail="Cannot get Admins")
    return get_all_admins


@router.get("/get-summary-applicants-interview", response_model=SummaryInterviewListPageResponse)
def get_sum_app_interview(db: Session = Depends(get_db)):
    get_sum_app_interview = crud.get_all_applicant_summary_interview_page(db)
    if not get_sum_app_interview:
        raise HTTPException(status_code=404, detail="Cannot get applicants information")
    return get_sum_app_interview


@router.get("/get-applicant-interview-eva/{applicant_id}/{committee_id}", response_model=EduInterviewEvaListResponse)
def get_applicant_interview_eva(applicant_id: str, committee_id: Optional[str] = None, db: Session = Depends(get_db)):
    get_applicant_interview_eva = crud.get_all_applicant_result_interview_eva_page(db, applicant_id, committee_id)
    if not get_applicant_interview_eva:
        raise HTTPException(status_code=404, detail="Cannot get applicants information")
    return get_applicant_interview_eva


@router.get("/get-applicant-interview-evas/{applicant_id}", response_model=EduInterviewEvaListResponse)
def get_applicant_interview_eva(applicant_id: str, db: Session = Depends(get_db)):
    get_applicant_interview_eva = crud.get_all_applicant_result_interview_eva_page(db, applicant_id)
    if not get_applicant_interview_eva:
        raise HTTPException(status_code=404, detail="Cannot get applicants information")
    return get_applicant_interview_eva

########## interview round ##########
@router.get("/get-interview-round", response_model=InterviewRoundListResponse)
def get_interview_round(db: Session = Depends(get_db)):
    return crud.get_interview_round(db)


@router.post("/create-interview-round", response_model=InterviewRoundResponse)
def create_interview_round(data: InterviewRoundResponse, db: Session = Depends(get_db)):
    return crud.create_interview_round(db, data)


@router.put("/update-interview-round/{interviewRoundId}", response_model=InterviewRoundUpdate)
def update_interview_round(interviewRoundId: str, data: InterviewRoundUpdate, db: Session = Depends(get_db)):
    update_interview_round = crud.update_interview_round(db, interviewRoundId, data)
    if not update_interview_round:
        raise HTTPException(status_code=404, detail="Interview Round Not Found")
    return update_interview_round
####################


########## interview room detail ##########
@router.get("/get-all-interview-room-detail", response_model=list[InterviewRoomDetailCreating])
def read_all_interview_room_detail(db: Session = Depends(get_db)):
    return crud.get_all_interview_room_detail(db)

@router.post("/create-interview-room-detail", response_model=InterviewRoomDetailCreating)
def create_interview_room_detail(data: InterviewRoomDetailCreating, db: Session = Depends(get_db)):
    return crud.create_interview_room_detail(db, data)


@router.put("/update-interview-room-detail", response_model=InterviewRoomDetailCreating)
def update_interview_room_detail(data: InterviewRoomDetailCreating, db: Session = Depends(get_db)):
    return crud.update_interview_room_detail(db, data)


@router.delete("/delete-interview-room-detail")
def delete_interview_room_detail(round_id: str, room_id: str, db: Session = Depends(get_db)):
    return crud.delete_interview_room_detail(db, round_id, room_id)
####################


########## interview room committee ##########
@router.get("/get-all-interview-room-committee", response_model=list[InterviewRoomCommitteeResponse])
def read_all_interview_room_committee(db: Session = Depends(get_db)):
    return crud.get_all_interview_room_committee(db)


@router.get("/get-one-interview-room-committee", response_model=list[InterviewRoomCommitteeResponse])
def read_one_interview_room_committee(room_id: str, db: Session = Depends(get_db)):
    return crud.get_one_interview_room_committee(db, room_id)


@router.post("/create-interview-room-committee", response_model=InterviewRoomCommitteeCreating)
def create_interview_room_committee(data: InterviewRoomCommitteeCreating, db: Session = Depends(get_db)):
    return crud.create_interview_room_committee(db, data)


@router.delete("/delete-interview-room-committee")
def delete_interview_room_committee(interview_room_id: str, db: Session = Depends(get_db)):
    return crud.delete_interview_room_committee(db, interview_room_id)
####################


@router.get("/get-interview-room-details", response_model=InterviewRoundDetailListResponse)
def get_all_interview_room_details(db: Session = Depends(get_db)):
    return crud.get_all_interview_room_details(db)


@router.get("/get-all-interview-rooms", response_model=InterviewRoomDetailsListResponse)
def get_all_rooms_api(db: Session = Depends(get_db)):
    rooms = crud.get_all_interview_rooms(db)
    if not rooms.room:
        raise HTTPException(status_code=404, detail="No interview rooms found")
    return rooms


@router.put("/update-applicant-status/{applicant_id}/{education_id}")
def created_or_updated_applicant_problem_status(
    applicant_id: str,
    education_id: str,
    data: str = Body(...),
    db: Session = Depends(get_db)
):
    problem = crud.create_or_updated_applicant_problem(db, applicant_id, education_id, data)

    return problem


@router.get("/get-applicant-problem/{applicant_id}", response_model=ApplicantInformationProblem)
def get_applicant_problem(applicant_id: str, db: Session = Depends(get_db)):
    applicant_problem = crud.get_applicant_information_problem(db, applicant_id)
    if not applicant_problem:
        raise HTTPException(status_code=404, detail="Applicant problem not found")
    return applicant_problem
