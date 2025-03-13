import requests
import os
from dotenv import load_dotenv


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
