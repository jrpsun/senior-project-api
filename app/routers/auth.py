from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.auth import (
    ApplicantCreate,
    ApplicantLoginRequest,
    AdminLoginRequest
)
from app.crud import auth as crud

router = APIRouter()



@router.post("/applicant/register")
def create_applicant(applicant_data: ApplicantCreate, db: Session = Depends(get_db)):
    return crud.create_applicant(db, applicant_data)


@router.post("/applicant/login")
def login_applicant(request: ApplicantLoginRequest, response: Response, db: Session = Depends(get_db)):
    return crud.applicant_login(response, db, request.idNumber, request.password)


@router.post("/admin/login")
def login_admin(request: AdminLoginRequest, response: Response, db: Session = Depends(get_db)):
    return crud.admin_login(response, db, request.email, request.password)