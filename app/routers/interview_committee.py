from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import interview_committee as crud
from app.schemas.interview_committee import (
    InterviewCommitteeCreate,
    InterviewCommitteeResponse,
    InterviewCommitteeUpdate,
    InterviewListApplicantDataMainPageResponse,
    InterviewEvaCreate,
    InterviewRoundCreate,
    InterviewRoomCreate,
    InterviewRoomUpdate,
    InterviewEvaUpdate,
    EditInterviewRoom
)


router = APIRouter()


@router.post("/", response_model=InterviewCommitteeResponse)
def create_ic(ic_data: InterviewCommitteeCreate, db: Session = Depends(get_db)):
    return crud.create_interview_committee(db, ic_data)


@router.get("/get-all-interviewC", response_model=list[InterviewCommitteeResponse])
def read_ics(db: Session = Depends(get_db)):
    return crud.get_interview_committees(db)


@router.get("/get-interviewC/{ic_id}", response_model=InterviewCommitteeResponse)
def read_ic(ic_id: str, db: Session = Depends(get_db)):
    ic = crud.get_interview_committee_by_id(db, ic_id)
    if not ic:
        raise HTTPException(status_code=404, detail="InterviewCommittee not found")
    return ic


@router.put("/update-interview-com/{ic_id}", response_model=InterviewCommitteeResponse)
def update_ic(ic_id: str, ic_data: InterviewCommitteeUpdate, db: Session = Depends(get_db)):
    updated_ic = crud.update_interview_committee(db, ic_id, ic_data)
    if not updated_ic:
        raise HTTPException(status_code=404, detail="InterviewCommittee not found")
    return updated_ic


@router.delete("/delete-interview-com/{ic_id}")
def delete_ic(ic_id: str, db: Session = Depends(get_db)):
    deleted_ic = crud.delete_interview_committee(db, ic_id)
    if not deleted_ic:
        raise HTTPException(status_code=404, detail="InterviewCommittee not found")
    return {"message": "InterviewCommittee deleted successfully"}


@router.get("/all-applicant-interviewC/{committee_id}", response_model=InterviewListApplicantDataMainPageResponse)
def read_all_applicants(committee_id: str, db: Session = Depends(get_db)):
    read_all_applicants = crud.get_all_applicants_interview_main_page(db, committee_id)
    if not read_all_applicants:
        raise HTTPException(status_code=404, detail="Applicant Information not found")
    return read_all_applicants


@router.get("/get-interviewEva/{applican_id}")
def get_interview_eva_info(applican_id: str, db: Session = Depends(get_db)):
    get_interview_eva_info = crud.get_interview_eva_page(db, applican_id)
    if not get_interview_eva_info:
        raise HTTPException(status_code=404, detail="Not found Interview Evaluation for applicant id {applican_id}")
    return get_interview_eva_info


@router.put("/update-interview-Eva")
def update_interview_Eva(app_id: str, com_id: str, adm_id: str, inEva_data: InterviewEvaUpdate, db: Session = Depends(get_db)):
    success = crud.update_interview_eva_to_applicant(db, app_id, com_id, adm_id, inEva_data)
    if not success:
        raise HTTPException(status_code=404, detail=f"Applicant id {app_id} not found")
    
    return {"status": "success", "message": "Interview evaluation updated successfully"}


@router.post("/create-interview-eva")
def create_int_eva(newEva_data: list[InterviewEvaCreate], db: Session = Depends(get_db)):  
    return crud.create_interview_eva(db, newEva_data)


@router.post("/create-interview-round")
def create_int_round(newEvaRound_data: InterviewRoundCreate, db: Session = Depends(get_db)):  
    return crud.create_interview_round(db, newEvaRound_data)


@router.put("/update-interview-round")
def update_int_round(round_id: str, EvaRound_data: InterviewRoundCreate, db: Session = Depends(get_db)):
    update_int_round = crud.update_interview_round(db, round_id, EvaRound_data)
    if not update_int_round:
        raise HTTPException(status_code=404, detail="Not found round id {round_id}")
    return update_int_round


@router.post("/create-interview-room")
def create_int_room(newIntRoom_data: InterviewRoomCreate, db: Session = Depends(get_db)):  
    return crud.create_interview_room(db, newIntRoom_data)


@router.put("/update-interview-room")
def update_int_room(room_id: str, EvaRoom_data: InterviewRoomUpdate, db: Session = Depends(get_db)):
    update_int_room = crud.update_interview_room(db, room_id, EvaRoom_data)
    if not update_int_room:
        raise HTTPException(status_code=404, detail="Failed to updating room")
    return update_int_room


@router.put("/update-interview-room-auto-grouping")
def update_int_room_auto_group(update_data: EditInterviewRoom, db: Session = Depends(get_db)):
    update_int_room_auto_group = crud.update_interview_room_auto_group(db, update_data)
    if not update_int_room_auto_group:
        raise HTTPException(status_code=404, detail="Failed to updating room")
    return update_int_room_auto_group
