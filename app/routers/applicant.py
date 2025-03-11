from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.applicant import (
    ApplicantCreate,
    ApplicantGeneralInformationResponse,
    ApplicantGeneralInformationUpdate,
)
from app.crud import applicant as crud

router = APIRouter()


@router.post("/")
def create_applicant(applicant_data: ApplicantCreate, db: Session = Depends(get_db)):
    return crud.create_applicant(db, applicant_data)


@router.put("/{applicant_id}", response_model=ApplicantGeneralInformationResponse)
def update_applicant_general_info(applicant_id: str, update_data: ApplicantGeneralInformationUpdate, db: Session = Depends(get_db)):
    updated_applicant_general = crud.update_applicant_general_info(db, applicant_id, update_data)
    if not updated_applicant_general:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return updated_applicant_general


@router.get("/{applicant_id}", response_model=ApplicantGeneralInformationResponse)
def get_applicant_general_info(applicant_id: str, db: Session = Depends(get_db)):
    applicant = crud.get_applicant_general_info(db, applicant_id)
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return applicant