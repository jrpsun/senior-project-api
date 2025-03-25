class Prompt:
    def certificate_prompt(extracted_texts: str):
        return f"""
            นี่คือผลลัพธ์จากการ ocr ใบ Certificate
            ```{extracted_texts}```
            ช่วยนำข้อมูลที่ถูกต้องลงใน json ที่กำหนดและ clenning ให้สวยงาม โดยหัวข้อใน json คือ
            - NameOfCompetition คือ ชื่อโครงการที่เข้าร่วม
            - YearOfCompetition คือ ปีที่เข้าร่วม
            - LevelOfCompetition แบ่งเป็น School, District, Provincial, Regional, National, International
            - AwardReceived ถ้าไม่มีให้ใส่ว่า เข้าร่วมการแข่งขัน
            - ProjectOrWorksName คือ โปรเจคที่ทำ
            ช่วย return ออกมาแค่ตัว json เท่านั้น
            """
    
    def identification_card_prompt(extracted_texts: str):
        return f"""
        นี่คือผลลัพธ์จากการ ocr บัตรปชช. ของไทย
        ``` {extracted_texts} ```
        ช่วยนำข้อมูลที่ถูกต้องลงใน json ที่กำหนดและ clenning ให้สวยงาม ถ้าไม่พบข้อมูลให้ใส่ null โดยหัวข้อใน json คือ
        - idCardExpDate คือ วันหมดอายุบัตร รูปแบบ 16 ม.ค. 2570
        - birthDate รูปแบบ 16 มี.ค. 2546
        ช่วย return ออกมาแค่ตัว json เท่านั้น
        """