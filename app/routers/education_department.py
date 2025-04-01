from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.education_department import (
    EducationDepartmentCreate,
    EducationDepartmentUpdate,
    EducationDepartmentResponse,
    EduListApplicantDataMainPageResponse
)
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
        raise HTTPException(status_code=404, detail="Education Department not found")
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

