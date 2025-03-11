from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.to_excel import create_excel
from app.models.applicant_general_information import ApplicantGeneralInformation

router = APIRouter()


@router.get("/export_excel")
async def export_excel(db: Session = Depends(get_db)):
    # ดึงข้อมูลจากฐานข้อมูล (สามารถใช้ CRUD function)
    data = db.query(ApplicantGeneralInformation).all()

    # สร้าง Excel file
    result = create_excel(data, "applicants.xlsx")
    return {"message": result}