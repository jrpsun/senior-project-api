from fastapi import APIRouter, File, UploadFile
from app.services.pdf import PDFProcessor
from app.services.ocr import OCRProcessor
from app.services.gemini import Gemini
from app.services.prompt import Prompt

router = APIRouter()

ocr_processor = OCRProcessor()


@router.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()

    extracted_texts = []

    if file.content_type == "application/pdf":
        image_bytes_list = PDFProcessor.pdf_to_images(file_bytes)
        for image_bytes in image_bytes_list:
            text = ocr_processor.ocr_space(image_bytes)
            if text:
                extracted_texts.append(text)

    elif file.content_type.startswith("image/"):
        text = ocr_processor.ocr_space(file_bytes)
        if text:
            extracted_texts.append(text)

    else:
        return {"error": "รองรับเฉพาะไฟล์ PDF"}
    
    prompt = Prompt.certificate_prompt(extracted_texts)
    result = Gemini.generate(prompt)

    return result
