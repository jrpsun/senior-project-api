from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.to_excel import create_excel, excel_applicant_list
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.crud import excel as crud
from fastapi.responses import StreamingResponse
from urllib.parse import quote

router = APIRouter()


@router.get("/export_excel")
async def export_excel(db: Session = Depends(get_db)):
    # ดึงข้อมูลจากฐานข้อมูล (สามารถใช้ CRUD function)
    data = db.query(ApplicantGeneralInformation).all()

    # สร้าง Excel file
    result = create_excel(data, "applicants.xlsx")
    return {"message": result}


@router.get("/applicant-list/{admissionId}")
async def applicant_list_excel(admissionId: str, db: Session = Depends(get_db)):
    applicant = crud.get_applicant_list(db, admissionId)
    admission = crud.get_admission_by_id(db, admissionId)

    excel_file = excel_applicant_list(applicant, admission)
    filename = f"applicant_list_{admission.roundName}.xlsx"
    quoted_filename = quote(filename)

    headers = {
        "Content-Disposition": f"attachment; filename*=UTF-8''{quoted_filename}"
    }

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )