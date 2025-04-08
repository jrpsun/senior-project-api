class Prompt:
    def award_cer_prompt(extracted_texts: str):
        return f"""
            นี่คือผลลัพธ์จากการ ocr ใบ Certificate award
            ```{extracted_texts}```
            ช่วยนำข้อมูลที่ถูกต้องลงใน json ที่กำหนดและ clenning ให้สวยงาม โดยหัวข้อใน json คือ
            - NameOfCompetition คือ ชื่อโครงการที่เข้าร่วม ถ้าไม่มีให้ใส่ ""
            - rewardYear คือ ปีที่เข้าร่วม แปลงเป็น ค.ศ. ด้วย ถ้าไม่มีให้ใส่ ""
            - rewardLevel แบ่งเป็น School, District, Provincial, Regional, National, International
            - rewardAwards ถ้าไม่มีให้ใส่ว่า เข้าร่วมการแข่งขัน
            - project คือ โปรเจคที่ทำ ถ้าไม่มีให้ใส่ ""
            ช่วย return ออกมาแค่ตัว json เท่านั้น
            """
    
    def talent_cer_prompt(extracted_texts: str):
        return f"""
            นี่คือผลลัพธ์จากการ ocr ใบ Certificate talent
            ```{extracted_texts}```
            ช่วยนำข้อมูลที่ถูกต้องลงใน json ที่กำหนดและ clenning ให้สวยงาม โดยหัวข้อใน json คือ
            - kindOfTalent คือ ประเภทของความสามารถพิเศษ แบ่งเป็น "athletic", "creative_innovation", "leadership_volunteering", "cultural"
            - nameOfCompetition คือ ชื่อผลงานหรือกิจกรรม ถ้าไม่มีให้ใส่ ""
            - talentYear คือ ปีที่เข้าร่วม แปลงเป็น ค.ศ. ด้วย ถ้าไม่มีให้ใส่ ""
            - talentAwards ถ้าไม่มีให้ใส่ว่า เข้าร่วมการแข่งขัน 
            ช่วย return ออกมาแค่ตัว json เท่านั้น
            """
    
    def train_cer_prompt(extracted_texts: str):
        return f"""
            นี่คือผลลัพธ์จากการ ocr ใบ Certificate training
            ```{extracted_texts}```
            ช่วยนำข้อมูลที่ถูกต้องลงใน json ที่กำหนดและ clenning ให้สวยงาม โดยหัวข้อใน json คือ     
            - nameOfCourse คือ ชื่อโปรแกรมที่เข้ารวม ถ้าไม่มีให้ใส่ ""
            - institution คือ สถาบัน/ผู้ให้บริการโปรแกรม ถ้าไม่มีให้ใส่ ""
            - trainingYear คือ ปีที่เข้าฝึก แปลงเป็น ค.ศ. ด้วย ถ้าไม่มีให้ใส่ ""
            - trainingMode คือ offline หรือ online
            ช่วย return ออกมาแค่ตัว json เท่านั้น
            """
    
    def identification_card_prompt(extracted_texts: str):
        return f"""
        นี่คือผลลัพธ์จากการ ocr บัตรปชช. ของไทย
        ``` {extracted_texts} ```
        ช่วยนำข้อมูลที่ถูกต้องลงใน json ที่กำหนดและ clenning ให้สวยงาม ถ้าไม่พบข้อมูลให้ใส่ null โดยหัวข้อใน json คือ
        - idCardExpDate คือ วันบัตรหมดอายุ รูปแบบเป็น 17/06/2000
        - birthDate รูปแบบ 16/12/1999
        ช่วย return ออกมาแค่ตัว json เท่านั้น
        """

    def transcript_ict_propmt(extracted_texts: str):
        return f"""
        นี่คือผลลัพธ์จากการ ocr transcript ของไทย
        ``` {extracted_texts} ```
        ช่วยนำข้อมูลที่ถูกต้องลงใน json ที่กำหนดและ clenning ให้สวยงาม ถ้าไม่พบข้อมูลให้ใส่ "" โดยหัวข้อใน json คือ
        - firstname คือ ชื่อจริงของเจ้าของ transcript string,
        - lastname คือ นามสกุลของเจ้าของ transcript string,
        - academicProvince คือ จังหวัดที่ตั้งสถานศึกษา string,
        - schoolName คือ ชื่อโรงเรียน string,
        - cumulativeGPA คือ เกรดเฉลี่ยสะสม ขอเป็น string เช่น "3.12",
        ช่วย return ออกมาแค่ตัว json เท่านั้น
        """