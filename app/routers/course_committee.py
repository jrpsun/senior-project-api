from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.course_committee import (
    CourseCommitteeCreate,
    CourseCommitteeUpdate,
    CourseCommitteeResponse,
)
from app.crud import course_committee as crud

router = APIRouter()


@router.post("/", response_model=CourseCommitteeResponse)
def create_committee(committee_data: CourseCommitteeCreate, db: Session = Depends(get_db)):
    return crud.create_course_committee(db, committee_data)


@router.get("/{committee_id}", response_model=CourseCommitteeResponse)
def read_committee(committee_id: str, db: Session = Depends(get_db)):
    committee = crud.get_course_committee(db, committee_id)
    if not committee:
        raise HTTPException(status_code=404, detail="Course Committee not found")
    return committee


@router.get("/", response_model=list[CourseCommitteeResponse])
def read_all_committees(db: Session = Depends(get_db)):
    return crud.get_all_course_committees(db)


@router.put("/{committee_id}", response_model=CourseCommitteeResponse)
def update_committee(committee_id: str, committee_data: CourseCommitteeUpdate, db: Session = Depends(get_db)):
    updated_committee = crud.update_course_committee(db, committee_id, committee_data)
    if not updated_committee:
        raise HTTPException(status_code=404, detail="Course Committee not found")
    return updated_committee


@router.delete("/{committee_id}")
def delete_committee(committee_id: str, db: Session = Depends(get_db)):
    deleted_committee = crud.delete_course_committee(db, committee_id)
    if not deleted_committee:
        raise HTTPException(status_code=404, detail="Course Committee not found")
    return {"message": "Course Committee deleted successfully"}