from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.schemas.admission import (
    AdmissionBase,
    AdmissionUpdate,
    AdmissionResponse,
)
from app.crud import admission as crud
from app.services.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=AdmissionResponse)
def create_admission(admission_data: AdmissionBase, db: Session = Depends(get_db)):
    return crud.create_admission(db, admission_data)


@router.get("/{admission_id}", response_model=AdmissionResponse)
def read_admission(admission_id: str, db: Session = Depends(get_db)):
    admission = crud.get_admission(db, admission_id)
    if not admission:
        raise HTTPException(status_code=404, detail="Admission not found")
    return admission


@router.get("/", response_model=list[AdmissionResponse])
def read_all_admissions(db: Session = Depends(get_db)):
    return crud.get_all_admissions(db)


@router.put("/{admission_id}", response_model=AdmissionResponse)
def update_admission(admission_id: str, admission_data: AdmissionUpdate, db: Session = Depends(get_db)):
    updated_admission = crud.update_admission(db, admission_id, admission_data)
    if not updated_admission:
        raise HTTPException(status_code=404, detail="Admission not found")
    return updated_admission


@router.delete("/{admission_id}")
def delete_admission(admission_id: str, db: Session = Depends(get_db)):
    deleted_admission = crud.delete_admission(db, admission_id)
    if not deleted_admission:
        raise HTTPException(status_code=404, detail="Admission not found")
    return {"message": "Admission deleted successfully"}