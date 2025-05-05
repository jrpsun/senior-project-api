from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.excel import ApplicantFilterCourseSummary, ApplicantFilterExcel
from app.services import to_excel as excel
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
    result = excel.create_excel(data, "applicants.xlsx")
    return {"message": result}


@router.post("/applicant-list")
async def applicant_list_excel(filter_data: ApplicantFilterExcel, db: Session = Depends(get_db)):
    admission = crud.get_admission_by_filter_data(db, filter_data)
    applicant = crud.get_applicant_list(db, admission.admissionId, filter_data)

    excel_file = excel.excel_applicant_list(applicant, admission, filter_data)
    filename = f"Applicant_List_{admission.roundName}_{admission.academicYear}.xlsx"
    quoted_filename = quote(filename)

    headers = {
        "Content-Disposition": f"attachment; filename*=UTF-8''{quoted_filename}"
    }

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )


@router.post("/screening-group")
async def applicant_screening_group_excel(filter_data: ApplicantFilterExcel, db: Session = Depends(get_db)):
    admission = crud.get_admission_by_filter_data(db, filter_data)
    applicant = crud.get_applicant_screening_group(db, admission.admissionId, filter_data)

    excel_file = excel.excel_screening_group(applicant, admission, filter_data)
    filename = f"Screening_Grouping_{admission.roundName}_{admission.academicYear}.xlsx"
    quoted_filename = quote(filename)

    headers = {
        "Content-Disposition": f"attachment; filename*=UTF-8''{quoted_filename}"
    }

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )


@router.post("/screening-summary")
async def applicant_screening_summary_excel(filter_data: ApplicantFilterCourseSummary, db: Session = Depends(get_db)):
    applicant = crud.get_applicant_screening_summary(db, filter_data)

    excel_file = excel.excel_screening_summary(applicant)

    filename = f"Screening_Summary.xlsx"
    quoted_filename = quote(filename)

    headers = {
        "Content-Disposition": f"attachment; filename*=UTF-8''{quoted_filename}"
    }

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )
