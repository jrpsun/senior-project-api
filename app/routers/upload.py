import os
from fastapi import APIRouter, BackgroundTasks, Depends, File, Request, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from requests import Session
from app.db import get_db
from app.services.download import export_applicants_to_zip
from app.services.pdf import PDFProcessor
from app.services.ocr import OCRProcessor
from app.services.gemini import Gemini
from app.services.prompt import Prompt

router = APIRouter()

ocr_processor = OCRProcessor()


@router.post("/certificate/{type_cer}")
async def upload_file(type_cer: str, file: UploadFile = File(...)):
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
    
    if type_cer == "reward":
        prompt = Prompt.award_cer_prompt(extracted_texts)
    elif type_cer == "talent":
        prompt = Prompt.talent_cer_prompt(extracted_texts)
    elif type_cer == "training":
        prompt = Prompt.train_cer_prompt(extracted_texts)
    else :
        return {"error": "Type Certificate Not Found"}

    result = Gemini.generate(prompt)
    print(extracted_texts)
    return result


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
        text = ocr_processor.ocr_tesseract(file_bytes, "eng+tha")
        if text:
            extracted_texts.append(text)

    else:
        return {"error": "รองรับเฉพาะไฟล์ PDF"}
    
    prompt = Prompt.identification_card_prompt(extracted_texts)
    result = Gemini.generate(prompt)
    
    return result


@router.post("/transcript-ict")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()

    extracted_texts = []

    if file.content_type == "application/pdf":
        image_bytes_list = PDFProcessor.pdf_to_images(file_bytes)
        img1 = ocr_processor.crop_top_third(image_bytes_list[0]) # debug image save_path="D:/work/Senior/senior-project-api/app/services/test/image_1_3.png"
        text1 = ocr_processor.ocr_tesseract(img1, "tha")
        if text1:
            extracted_texts.append(text1)

        img2 = ocr_processor.crop_without_top_bottom_third(image_bytes_list[1])
        text2 = ocr_processor.ocr_tesseract(img2, "tha")
        if text2:
            extracted_texts.append(text2)
    
    prompt = Prompt.transcript_ict_propmt(extracted_texts)
    result = Gemini.generate(prompt)
    
    return result


@router.post("/download-applicants")
async def download_applicants(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    body = await request.json()
    zip_path = export_applicants_to_zip(body, db)
    # response = FileResponse(
    #     zip_path,
    #     filename="Applicants.zip",
    #     media_type="application/zip"
    # )

    # @response.call_on_close
    # def cleanup():
    #     try:
    #         os.remove(zip_path)
    #         print(f"Deleted zip file: {zip_path}")
    #     except Exception as e:
    #         print(f"Error deleting zip file: {e}")

    # return response

    # def iterfile():
    #     with open(zip_path, mode="rb") as file:
    #         yield from file
    #     os.remove(zip_path)  # ลบไฟล์หลังจากส่งจบแล้ว
    #     print(f"Deleted zip file: {zip_path}")

    # return StreamingResponse(iterfile(), media_type="application/zip", headers={
    #     "Content-Disposition": "attachment; filename=Applicants.zip"
    # })

    background_tasks.add_task(os.remove, zip_path)
    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename="selected_applicants.zip",
        background=background_tasks
    )