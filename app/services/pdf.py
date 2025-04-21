import fitz
import io
from PIL import Image, ImageEnhance, ImageFilter
import os
import numpy as np
import cv2

class PDFProcessor:
    @staticmethod
    def pdf_to_images(pdf_bytes):
        """ แปลง PDF เป็นภาพจาก bytes """
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        image_bytes_list = []

        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            
            # แปลง Pixmap เป็น PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # เพิ่มความคมชัด
            # enhancer = ImageEnhance.Sharpness(img)
            # img = enhancer.enhance(1.5)  # เพิ่มความคมชัด 1.5 เท่า

            # # เพิ่มความเข้ม
            # enhancer = ImageEnhance.Contrast(img)
            # img = enhancer.enhance(1.2)  # เพิ่มความเข้ม 1.2 เท่า

            # แปลง PIL Image เป็น bytes
            img_bytes_io = io.BytesIO()
            img.save(img_bytes_io, format="PNG")
            img_bytes_io.seek(0)

            image_bytes_list.append(img_bytes_io.getvalue())  # เพิ่ม bytes เข้า list

        pdf_document.close()
        return image_bytes_list  # คืนค่าเป็น list ของ bytes
    
    @staticmethod
    def pdf_to_images2(pdf_bytes):
        """ 
        แปลง PDF เป็นภาพอัจฉริยะ 
        - ปรับปรุงคุณภาพสำหรับ PDF ที่ไม่ชัด
        - แปลงปกติสำหรับ PDF ที่ชัดอยู่แล้ว
        """
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        image_bytes_list = []

        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            
            # เริ่มด้วยความละเอียดมาตรฐาน
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), dpi=300)
            
            # แปลง Pixmap เป็น PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # วิเคราะห์ความคมชัดของภาพ
            img_array = np.array(img)
            
            # คำนวณความคมชัดโดยใช้ Laplacian
            laplacian = cv2.Laplacian(cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY), cv2.CV_64F).var()
            
            # ถ้าภาพไม่คมชัด (ค่า variance ต่ำ) ให้ปรับปรุง
            if laplacian < 50:  # เกณฑ์ความคมชัดสามารถปรับได้
                # เพิ่มความคมชัด
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(2.0)  # เพิ่มความคมชัดมากขึ้น
                
                # เพิ่มความเข้ม
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.5)
                
                # กรองแบบ unsharp mask เพิ่มความคมชัด
                img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=250, threshold=3))

                print("bad bad bad:", page_number)
            
            # แปลง PIL Image เป็น bytes
            img_bytes_io = io.BytesIO()
            img.save(img_bytes_io, format="PNG", optimize=True)
            img_bytes_io.seek(0)

            image_bytes_list.append(img_bytes_io.getvalue())

        pdf_document.close()
        return image_bytes_list