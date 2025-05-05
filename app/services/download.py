from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.models import *
from app.db import get_db
import os, shutil, zipfile, uuid
import base64
import re


def save_file(folder_path: str, file_data: str | None, file_name: str | None):
    if not file_data or not file_name:
        return

    try:
        if file_data.startswith("data:"):
            header, base64_data = file_data.split(",", 1)
            decoded = base64.b64decode(base64_data)

            match = re.match(r"data:(.*?);base64", header)
            mime_type = match.group(1) if match else None

            if "." not in file_name and mime_type:
                ext = mime_type.split("/")[-1]
                file_name += f".{ext}"

        else:
            decoded = base64.b64decode(file_data)
    except Exception as e:
        print(f"Error decoding file: {e}")
        return

    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "wb") as f:
        f.write(decoded)


def export_applicants_to_zip(applicants: list[dict], db: Session):
    temp_folder = f"Applicants"
    os.makedirs(temp_folder, exist_ok=True)

    for app in applicants:
        appId = app["applicantId"]
        admId = app["admissionId"]

        regis_info = db.query(ApplicantRegistrations).filter_by(applicantId=appId).first()
        admission_info = db.query(Admission).filter_by(admissionId=admId).first()

        if not regis_info:
            raise HTTPException(status_code=404, detail=f"Applicant with ID: {appId} Not Found")
        
        if not admission_info:
            raise HTTPException(status_code=404, detail=f"Admission with ID: {admId} Not Found")

        folder_path = os.path.join(temp_folder, f"{admission_info.program}_{admission_info.roundName}_{admission_info.academicYear}_Applicant_{appId}_{regis_info.firstnameEN}_{regis_info.lastnameEN}")
        os.makedirs(folder_path, exist_ok=True)


        gen_info = db.query(ApplicantGeneralInformation).filter_by(
            applicantId=appId,
            programRegistered=admId
        ).first()

        if gen_info:
            save_file(folder_path, gen_info.applicantPicture, f"Picture_{gen_info.applicantId}_{regis_info.firstnameEN}_{regis_info.lastnameEN}.jpg")
            save_file(folder_path, gen_info.docCopyIdCard, gen_info.docCopyIdCardName)
            save_file(folder_path, gen_info.docCopyPassport, gen_info.docCopyPassportName)
            save_file(folder_path, gen_info.docCopyHouseRegis, gen_info.docCopyHouseRegisName)


        academic_info = db.query(ApplicantAcademicBackground).filter_by(
            applicantId=appId,
            programRegistered=admId
        ).first()

        if academic_info:
            save_file(folder_path, academic_info.docCopyTrans, academic_info.docCopyName)

        
        english_info = db.query(ApplicantEnglishExam).filter_by(
            applicantId=appId,
            programRegistered=admId
        ).first()

        if english_info:
            save_file(folder_path, english_info.enCer, english_info.enCerName)


        math_info = db.query(ApplicantMathematicsExam).filter_by(
            applicantId=appId,
            programRegistered=admId
        ).first()

        if math_info:
            save_file(folder_path, math_info.mathCer, math_info.mathCerName)
        

        doc_info = db.query(ApplicantAdditionalDocuments).filter_by(
            applicantId=appId,
            programRegistered=admId
        ).first()
        
        if doc_info:
            save_file(folder_path, doc_info.stateOfPurpose, doc_info.stateOfPurposeName)
            save_file(folder_path, doc_info.portfolio, doc_info.portfolioName)
            save_file(folder_path, doc_info.applicantResume, doc_info.applicantResumeName)
            save_file(folder_path, doc_info.additional, doc_info.additionalName)


        rewards = db.query(ApplicantReward).filter_by(
            applicantId=appId,
            programRegistered=admId
        ).all()

        if rewards:
            reward_folder = os.path.join(folder_path, "Computer Certificate")
            os.makedirs(reward_folder, exist_ok=True)
            for i, reward in enumerate(rewards, start=1):
                file_name = f"Com_Cert_{i}_{appId}_{regis_info.firstnameEN}_{regis_info.lastnameEN}"
                save_file(reward_folder, reward.rewardCer, file_name)


        talents = db.query(ApplicantTalent).filter_by(
            applicantId=appId,
            programRegistered=admId
        ).all()

        if talents:
            talent_folder = os.path.join(folder_path, "Talent Certificate")
            os.makedirs(talent_folder, exist_ok=True)
            for i, talent in enumerate(talents, start=1):
                file_name = f"Talent_Cert_{i}_{appId}_{regis_info.firstnameEN}_{regis_info.lastnameEN}"
                save_file(talent_folder, talent.talentCer, file_name)

        
        trains = db.query(ApplicantTraining).filter_by(
            applicantId=appId,
            programRegistered=admId
        ).all()

        if trains:
            train_folder = os.path.join(folder_path, "Training Certificate")
            os.makedirs(train_folder, exist_ok=True)
            for i, train in enumerate(trains, start=1):
                file_name = f"Training_Cert_{i}_{appId}_{regis_info.firstnameEN}_{regis_info.lastnameEN}"
                save_file(train_folder, train.trainingCer, file_name)

    
    zip_filename = f"{temp_folder}.zip"
    shutil.make_archive(temp_folder, 'zip', temp_folder)
    shutil.rmtree(temp_folder)

    return zip_filename


        


