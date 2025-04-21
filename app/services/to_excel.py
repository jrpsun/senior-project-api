from openpyxl import Workbook
from openpyxl.styles import Font
from typing import List, Optional
from datetime import datetime
from babel.dates import format_date
from io import BytesIO

from app.models.admission import Admission

def create_excel(data: List[dict], file_name: str):
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "หน้ารายชื่อผู้สมัคร"

    ws1.cell(row=1, column=1, value="รายชื่อผู้สมัครหลักสูตร ITCS/B - รอบ 1/68 - ICT Portfolio")
    ws1.cell(row=2, column=1, value="วันที่ส่งออก: 10 กุมภาพันธ์ 2025")
    ws1.cell(row=3, column=1, value="หลักสูตร: ITCS/B")
    ws1.cell(row=4, column=1, value="รอบสมัคร: 1/68 - ICT Portfolio")
    ws1.cell(row=5, column=1, value="สถานะการสมัคร: ทั้งหมด")
    ws1.cell(row=6, column=1, value="สถานะการชำระเงิน: ทั้งหมด")
    ws1.cell(row=7, column=1, value="จำนวนผู้สมัคร: 9 คน")
    
    headers = ["ลำดับที่", "ชื่อ", "นามสกุล", "วันเกิด"]
    
    for col, header in enumerate(headers, start=1):
        ws1.cell(row=9, column=col, value=header).font = Font(bold=True)

    for row, item in enumerate(data, start=10):
        ws1.cell(row=row, column=1, value=row-9)   
        ws1.cell(row=row, column=2, value=item.firstnameTH)
        ws1.cell(row=row, column=3, value=item.lastnameTH)
        ws1.cell(row=row, column=4, value=item.birthDate)

    ws2 = wb.create_sheet(title="หน้าจัดหลุ่มประเมิณเบื้องต้น")
    ws2.cell(row=1, column=1, value="อันนี้คือหน้าจัดหลุ่มนะจร๊ะ หรือก็คือหน้า 2 นั่นเอง")

    wb.save(file_name)
    return f"{file_name} saved successfully."


def excel_applicant_list(applicant: List[dict], admission: Optional[Admission]):
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "sheet 1"

    today = format_date(datetime.now(), format='d MMMM y', locale='th')

    ws1.cell(row=1, column=1, value=f"ราบชื่อผู้สมัครหลักสูตร {admission.program} - {admission.roundName}").font = Font(bold=True, name="Sarabun")
    ws1.cell(row=2, column=1, value=f"วันที่ส่งออก: {today}").font = Font(bold=True, name="Sarabun")
    ws1.cell(row=3, column=1, value=f"หลักสูตร: {admission.program}").font = Font(bold=True, name="Sarabun")
    ws1.cell(row=4, column=1, value=f"รอบสมัคร: {admission.roundName}").font = Font(bold=True, name="Sarabun")
    ws1.cell(row=5, column=1, value=f"สถานะการสมัคร: ").font = Font(bold=True, name="Sarabun")
    ws1.cell(row=6, column=1, value=f"สถานะการชำระเงิน: ").font = Font(bold=True, name="Sarabun")
    ws1.cell(row=7, column=1, value=f"จำนวนผู้สมัครทั้งหมด: {len(applicant)}").font = Font(bold=True, name="Sarabun")

    headers = ["ลำดับที่", "หลักสูตร", "รอบการสมัคร", "เลขที่สมัคร", "ชื่อ - นามสกุล ผู้สมัคร", "โรงเรียน", "CGPA", "GPA Math", "GPA English", "GPA Sc and Techno",
               "สถานะการสมัคร", "สถานะเอกสาร", "สถานะการชำระเงิน", "อีเมล", "โทรศัพท์", "วันที่สมัคร"]
    
    for col, header in enumerate(headers, start=1):
        ws1.cell(row=9, column=col, value=header).font = Font(bold=True, name="Sarabun")
    
    for row, item in enumerate(applicant, start=10):
        ws1.cell(row=row, column=1, value=row-9).font = Font(name="Sarabun")
        ws1.cell(row=row, column=2, value=admission.program).font = Font(name="Sarabun")
        ws1.cell(row=row, column=3, value=admission.roundName).font = Font(name="Sarabun")
        ws1.cell(row=row, column=4, value=item["applicantId"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=5, value=item["name"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=6, value=item["school"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=7, value=item["cgpa"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=8, value=item["dst_m"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=9, value=item["dst_e"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=10, value=item["dst_s"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=11, value=item["admissionStatus"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=12, value=item["docStatus"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=13, value=item["paymentStatus"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=14, value=item["email"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=15, value=item["phone"]).font = Font(name="Sarabun")
        ws1.cell(row=row, column=16, value=item["applyDate"]).font = Font(name="Sarabun")


    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return output




