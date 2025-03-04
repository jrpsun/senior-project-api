from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import interview_committee as crud
from app.schemas.interview_committee import (
    InterviewCommitteeCreate,
    InterviewCommitteeResponse,
    InterviewCommitteeUpdate
)
router = APIRouter()


@router.post("/", response_model=InterviewCommitteeResponse)
def create_ic(ic_data: InterviewCommitteeCreate, db: Session = Depends(get_db)):
    return crud.create_interview_committee(db, ic_data)


@router.get("/", response_model=list[InterviewCommitteeResponse])
def read_ics(db: Session = Depends(get_db)):
    return crud.get_interview_committees(db)


@router.get("/{ic_id}", response_model=InterviewCommitteeResponse)
def read_ic(ic_id: str, db: Session = Depends(get_db)):
    ic = crud.get_interview_committee_by_id(db, ic_id)
    if not ic:
        raise HTTPException(status_code=404, detail="InterviewCommittee not found")
    return ic


@router.put("/{ic_id}", response_model=InterviewCommitteeResponse)
def update_ic(ic_id: str, ic_data: InterviewCommitteeUpdate, db: Session = Depends(get_db)):
    updated_ic = crud.update_interview_committee(db, ic_id, ic_data)
    if not updated_ic:
        raise HTTPException(status_code=404, detail="InterviewCommittee not found")
    return updated_ic


@router.delete("/{ic_id}")
def delete_ic(ic_id: str, db: Session = Depends(get_db)):
    deleted_ic = crud.delete_interview_committee(db, ic_id)
    if not deleted_ic:
        raise HTTPException(status_code=404, detail="InterviewCommittee not found")
    return {"message": "InterviewCommittee deleted successfully"}