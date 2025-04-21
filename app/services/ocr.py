import requests
import os
from dotenv import load_dotenv
from PIL import Image
import io
import pytesseract
import cv2
import numpy as np


class OCRProcessor:
    @staticmethod
    def ocr_space(image_bytes):
        """ ส่งภาพเป็น bytes เข้า OCR API """
        load_dotenv()
        url = 'https://api.ocr.space/parse/image'
        payload = {
            'apikey': os.getenv("OCR_SPACE_API_KEY"),
            'language': os.getenv("OCR_LANGUAGE", "auto"),
            'OCREngine': int(os.getenv("OCR_ENGINE", 2)),
        }
        files = {'file': ('image.png', image_bytes, 'image/png')}

        response = requests.post(url, files=files, data=payload)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('IsErroredOnProcessing', False):
                print(f"Error: {result.get('ErrorMessage')}")
                return None
            else:
                return result['ParsedResults'][0]['ParsedText']
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return None
    
    @staticmethod
    def ocr_tesseract(image_bytes, lang: str):
        load_dotenv()
        pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
        try:
            image = Image.open(io.BytesIO(image_bytes))

            text = pytesseract.image_to_string(image, lang=lang)

            return text.strip()
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    def find_card(image):
        try:
            if image is None:
                raise ValueError("ไม่สามารถถอดรหัสรูปภาพได้")

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 30, 200)
            contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

            id_card_contour = None
            for contour in contours:
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
                if len(approx) == 4:
                    id_card_contour = approx
                    break

            if id_card_contour is None:
                raise ValueError("ไม่พบขอบสี่เหลี่ยมของบัตรประชาชน")

            # ปรับมุมมอง
            points = id_card_contour.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")
            s = points.sum(axis=1)
            rect[0] = points[np.argmin(s)]
            rect[2] = points[np.argmax(s)]
            diff = np.diff(points, axis=1)
            rect[1] = points[np.argmin(diff)]
            rect[3] = points[np.argmax(diff)]

            (tl, tr, br, bl) = rect
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            maxWidth = max(int(widthA), int(widthB))

            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            maxHeight = max(int(heightA), int(heightB))

            dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
            M = cv2.getPerspectiveTransform(rect, dst)
            cropped_image = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

            return cropped_image

        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}")
            return None
    
    @staticmethod
    def draw_all_contours(image):
        try:
            # แปลงรูปภาพเป็นสีเทา
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # ตรวจจับขอบ
            edged = cv2.Canny(gray, 30, 200)

            # หาเส้นขอบทั้งหมด
            contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # วาดกรอบสี่เหลี่ยมรอบเส้นขอบทั้งหมด
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # วาดกรอบสีเขียว

            cv2.imwrite("cropped_card.jpg", image)

        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}")
    
    @staticmethod
    def remove_empty_area(image):
        """ ตัดพื้นที่ที่ไม่มีตัวอักษรออกไป """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # แปลงเป็นขาวดำ
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # ลด noise
        thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # แปลงเป็นขาวดำโดยใช้ thresholding

        # หาขอบเขตของพื้นที่ที่มีข้อความ (Contours)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # สร้าง mask สำหรับพื้นที่ที่มีข้อความ
        mask = np.zeros(gray.shape, dtype=np.uint8)  # สร้าง mask ที่มีขนาดเท่ากับภาพเดิม แต่เต็มไปด้วยสีดำ

        for contour in contours:
            if cv2.contourArea(contour) > 500:  # กรองคอนทัวร์ที่เล็กเกินไป (อาจจะเป็น noise)
                cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)  # วาดพื้นที่ที่มีข้อความ

        # ใช้ mask ตัดพื้นที่ที่ไม่มีข้อความออก
        result = cv2.bitwise_and(image, image, mask=mask)

        # บันทึกหรือแสดงผลภาพที่ตัดส่วนที่ไม่มีข้อความออก
        cv2.imwrite("masked_card.jpg", result)

        return result


    @staticmethod
    def ocr_card(image_bytes):
        """ OCR บัตรโดยอัตโนมัติ """
        try:
            # แปลง bytes เป็น OpenCV image
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # ค้นหาบัตร
            # image_copy = image.copy()
            # OCRProcessor.draw_all_contours(image_copy)
            # card = OCRProcessor.find_card(image)
            card = OCRProcessor.remove_empty_area(image)
            if card is None:
                return "Error: ไม่พบบัตรในภาพ"

            # ขยายภาพบัตรให้ชัดขึ้น
            card_resized = cv2.resize(card, (card.shape[1] * 2, card.shape[0] * 2), interpolation=cv2.INTER_CUBIC)

            # แปลงเป็น PIL Image เพื่อใช้กับ pytesseract
            card_pil = Image.fromarray(cv2.cvtColor(card_resized, cv2.COLOR_BGR2RGB))

            # OCR เฉพาะบัตร
            text = pytesseract.image_to_string(card_pil, lang="tha+eng")

            return text.strip()
        except Exception as e:
            return f"Error: {str(e)}"
        
    
    @staticmethod
    def crop_thai_id_card_from_bytes(image_bytes):
        # แปลง byte เป็นอาร์เรย์
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # อ่านรูปภาพจาก numpy array
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # แสดงขนาดภาพเดิม
        print(f"Original image size: {image.shape}")
        
        # แปลงเป็นภาพขาวดำ
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # ทำให้ภาพคมชัดขึ้น - ลองวิธีต่างๆ
        # เมื่อก่อนใช้ THRESH_BINARY_INV + THRESH_OTSU
        # ลองวิธีอื่นๆ
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, 
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                    cv2.THRESH_BINARY_INV, 11, 2)
        
        # ค้นหา contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # แสดงจำนวน contours
        print(f"Number of contours found: {len(contours)}")
        
        # เรียงลำดับ contours ตามขนาด
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # เลือก contour ที่เป็นบัตรประชาชน
        for i, contour in enumerate(contours):
            # คำนวณพื้นที่และรูปร่าง
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            # แสดงรายละเอียด contour
            print(f"Contour {i}: Area = {area}, Approx points = {len(approx)}")
            
            # เงื่อนไขสำหรับบัตรประชาชน 
            # ลดความเข้มงวดลง
            if len(approx) == 4 and area > 10000:
                # หา bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # crop รูปภาพ
                padding = 500  # เพิ่มช่องว่างเล็กน้อย
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = min(w + 2*padding, image.shape[1] - x)
                h = min(h + 2*padding, image.shape[0] - y)
                
                cropped = image[y:y+h, x:x+w]
                
                print("Cropped successfully!")
                return cropped
        
        # ถ้าไม่พบ
        print("No suitable contour found!")
        return image  # ส่งคืนภาพเดิมถ้าไม่สามารถ crop ได้

    @staticmethod
    def perform_ocr(image):
        load_dotenv()
        pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
        # การตั้งค่า Tesseract สำหรับภาษาไทย
        custom_config = r'--oem 3 --psm 6 -l tha+eng'
        
        # ทำ OCR
        text = pytesseract.image_to_string(image, config=custom_config)
        
        return text

    @staticmethod
    def process_id_card_bytes(image_bytes):
        # crop รูปภาพ
        cropped_image = OCRProcessor.crop_thai_id_card_from_bytes(image_bytes)
        
        # บันทึกรูปที่ crop (ถ้าต้องการ)
        # cv2.imwrite('cropped_id_card.jpg', cropped_image)
        
        # ทำ OCR
        ocr_result = OCRProcessor.perform_ocr(cropped_image)
        return ocr_result


    @staticmethod
    def crop_top_third(image_bytes):
        # แปลง bytes เป็นรูปภาพ
        image = Image.open(io.BytesIO(image_bytes))
        
        # คำนวณความสูงของรูป
        width, height = image.size
        crop_height = height // 3.5
        
        # ตัดรูปจากด้านบน 1/3
        cropped_image = image.crop((0, 0, width, crop_height))
        
        # แปลงรูปกลับเป็น bytes
        byte_arr = io.BytesIO()
        cropped_image.save(byte_arr, format=image.format)
        
        return byte_arr.getvalue()
    
    @staticmethod
    def crop_without_top_bottom_third(image_bytes):
        image = Image.open(io.BytesIO(image_bytes))
        
        width, height = image.size
        
        start_y = height // 5
        end_y = height * 3 // 5

        cropped_image = image.crop((0, start_y, width, end_y))
    
        byte_arr = io.BytesIO()
        cropped_image.save(byte_arr, format=image.format)
        
        return byte_arr.getvalue()
        

