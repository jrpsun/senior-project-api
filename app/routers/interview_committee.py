from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import interview_committee as crud
from app.schemas.interview_committee import (
    InterviewCommitteeCreate,
    InterviewCommitteeResponse,
    InterviewCommitteeUpdate,
    InterviewListApplicantDataMainPageResponse
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


@router.put("/update-interviewC/{ic_id}", response_model=InterviewCommitteeResponse)
def update_ic(ic_id: str, ic_data: InterviewCommitteeUpdate, db: Session = Depends(get_db)):
    updated_ic = crud.update_interview_committee(db, ic_id, ic_data)
    if not updated_ic:
        raise HTTPException(status_code=404, detail="InterviewCommittee not found")
    return updated_ic


@router.delete("/delete-interviewC/{ic_id}")
def delete_ic(ic_id: str, db: Session = Depends(get_db)):
    deleted_ic = crud.delete_interview_committee(db, ic_id)
    if not deleted_ic:
        raise HTTPException(status_code=404, detail="InterviewCommittee not found")
    return {"message": "InterviewCommittee deleted successfully"}


@router.get("/all-applicant-interviewC", response_model=InterviewListApplicantDataMainPageResponse)
def read_all_applicants(db: Session = Depends(get_db)):
    read_all_applicants = crud.get_all_applicants_interview_main_page(db)
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
def update_interview_Eva(
    app_id: str, com_id: str, e_score: int, p_score: int, i_score: int, c_score: int, t_score: int, comment: str, 
    result: str, er: str, pr: str, ir: str, cr: str, tr: str,
    db: Session = Depends(get_db)
    ):
    update_interview_Eva = crud.update_interview_eva_to_applicant(
        db, app_id: str, com_id: str, e_score: int, p_score: int, i_score: int, c_score: int, t_score: int, comment: str,
        result: str, er: str, pr: str, ir: str, cr: str, tr: str
    )
    if not update_interview_Eva:
        raise HTTPException(status_code=404, detail="Not found applicant id {app_id}")
    return update_interview_Eva