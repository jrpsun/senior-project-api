from openpyxl import Workbook
from openpyxl.styles import Font
from typing import List

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
