from fastapi import APIRouter, File, UploadFile
from app.services.pdf import PDFProcessor
from app.services.ocr import OCRProcessor
from app.services.gemini import Gemini
from app.services.prompt import Prompt

router = APIRouter()

ocr_processor = OCRProcessor()


@router.post("/certificate/")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()

    extracted_texts = []

    if file.content_type == "application/pdf":
        image_bytes_list = PDFProcessor.pdf_to_images(file_bytes)
        for image_bytes in image_bytes_list:
            text = ocr_processor.ocr_tesseract(image_bytes, "eng+tha")
            if text.strip():
                extracted_texts.append(text)
        print("text:", extracted_texts)

    elif file.content_type.startswith("image/"):
        text = ocr_processor.ocr_tesseract(file_bytes, "eng+tha")
        if text:
            extracted_texts.append(text)

    else:
        return {"error": "รองรับเฉพาะไฟล์ PDF"}
    
    #prompt = Prompt.certificate_prompt(extracted_texts)
    #result = Gemini.generate(prompt)

    return extracted_texts


@router.post("/identification-card/")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()

    extracted_texts = []

    if file.content_type == "application/pdf":
        image_bytes_list = PDFProcessor.pdf_to_images(file_bytes)
        for image_bytes in image_bytes_list:
            text = ocr_processor.process_id_card_bytes(image_bytes)
            if text:
                extracted_texts.append(text)

    elif file.content_type.startswith("image/"):
        text = ocr_processor.process_id_card_bytes(file_bytes)
        if text:
            extracted_texts.append(text)

    else:
        return {"error": "รองรับเฉพาะไฟล์ PDF"}
    
    prompt = Prompt.identification_card_prompt(extracted_texts)
    result = Gemini.generate(prompt)

    return result


@router.post("/transcript")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()

    extracted_texts = []

    if file.content_type == "application/pdf":
        image_bytes_list = PDFProcessor.pdf_to_images(file_bytes)
        img1 = ocr_processor.crop_top_third(image_bytes_list[0], save_path="D:/work/Senior/senior-project-api/app/services/test/image_1_2.png") # debug image save_path="D:/work/Senior/senior-project-api/app/services/test/image_1_3.png"
        text1 = ocr_processor.ocr_tesseract(img1, "tha")
        if text1:
            extracted_texts.append(text1)

        img2 = ocr_processor.crop_without_top_bottom_third(image_bytes_list[1], save_path="D:/work/Senior/senior-project-api/app/services/test/image_2_2.png")
        text2 = ocr_processor.ocr_tesseract(img2, "tha")
        if text2:
            extracted_texts.append(text2)
    
    return extracted_texts
