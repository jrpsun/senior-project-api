from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.schemas.applicant import *
from app.crud import applicant as crud
from app.services.auth import get_current_user, perform_refresh_token

router = APIRouter()


@router.put("/general/{applicant_id}")
def update_applicant_general_info(applicant_id: str, update_data: ApplicantGeneralInformationUpdate, db: Session = Depends(get_db)):
    updated_applicant_general = crud.update_applicant_general_info(db, applicant_id, update_data)
    if not updated_applicant_general:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return updated_applicant_general


@router.get("/general/{applicant_id}", response_model=ApplicantGeneralInformationResponse)
def get_applicant_general_info(applicant_id: str, db: Session = Depends(get_db)):
    applicant = crud.get_applicant_general_info(db, applicant_id)
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return applicant


@router.put("/education/{applicant_id}")
def update_applicant_education_info(applicant_id: str, update_data: ApplicantEducationinfoUpdate, db: Session = Depends(get_db)):
    updated_applicant_education = crud.update_applicant_education_info(db, applicant_id, update_data)
    if not updated_applicant_education:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return updated_applicant_education


@router.get("/education/{applicant_id}", response_model=ApplicantEducationInfoResponse)
def get_applicant_education_info(applicant_id: str, db: Session = Depends(get_db)):
    applicant = crud.get_applicant_education_info(db, applicant_id)
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return applicant


@router.put("/reward")
def create_applicant_reward(update_data: list[ApplicantRewardResponse], db: Session = Depends(get_db)):
    new_applicant_reward = crud.process_applicant_rewards(db, update_data)
    if not new_applicant_reward:
        raise HTTPException(status_code=404, detail="Create Applicant Reward Failed")
    return new_applicant_reward


@router.get("/reward/{applicant_id}", response_model=list[ApplicantRewardResponse])
def get_rewards_by_appId(applicant_id: str, db: Session = Depends(get_db)):
    rewards = crud.get_rewards_by_applicant_id(db, applicant_id)
    if not rewards:
        return []
    return rewards


@router.delete("/reward/{reward_id}")
def delete_reward_by_id(reward_id: str, db: Session = Depends(get_db)):
    success = crud.delete_reward_by_id(db, reward_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Reward with id {reward_id} not found")
    return None


@router.put("/talent")
def created_or_updated_talent(updated_data: list[ApplicantTalentResponse], db: Session = Depends(get_db)):
    applicant_talent = crud.process_applicant_talents(db, updated_data)
    if not applicant_talent:
        raise HTTPException(status_code=404, detail="Created or Updated Applicant Talent Failed")
    return applicant_talent


@router.get("/talent/{applicant_id}", response_model=list[ApplicantTalentResponse])
def get_talents_by_appId(applicant_id: str, db: Session = Depends(get_db)):
    talents = crud.get_talents_by_applicant_id(db, applicant_id)
    if not talents:
        return []
    return talents


@router.delete("/talent/{talent_id}")
def delete_talent_by_id(talent_id: str, db: Session = Depends(get_db)):
    success = crud.delete_talent_by_id(db, talent_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Talent with id {talent_id} not found")
    return None


@router.put("/training")
def created_or_updated_training(updated_data: list[ApplicantTrainingResponse], db: Session = Depends(get_db)):
    applicant_training = crud.process_applicant_trainings(db, updated_data)
    if not applicant_training:
        raise HTTPException(status_code=404, detail="Created or Updated Applicant Training Failed")
    return applicant_training


@router.get("/training/{applicant_id}", response_model=list[ApplicantTrainingResponse])
def get_trining_by_appId(applicant_id: str, db: Session = Depends(get_db)):
    trains = crud.get_trains_by_applicant_id(db, applicant_id)
    if not trains:
        return []
    return trains


@router.delete("/training/{training_id}")
def delete_training_by_id(training_id: str, db: Session = Depends(get_db)):
    success = crud.delete_train_by_id(db, training_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Training with id {training_id} not found")
    return None


# Document
@router.put("/document/{applicant_id}")
def updated_applicant_document(applicant_id: str, updated_data: ApplicantDocumentsResponse, db: Session = Depends(get_db)):
    document = crud.updated_applicant_document(db, applicant_id, updated_data)
    if not document:
        raise HTTPException(status_code=404, detail=f"Updated Applicant Document with ID: {applicant_id} Failed")
    return document


@router.get("/document/{applicant_id}", response_model=ApplicantDocumentsResponse)
def get_applicant_document_by_id(applicant_id: str, db: Session = Depends(get_db)):
    document = crud.get_applicant_document(db, applicant_id)
    if not document:
        raise HTTPException(status_code=404, detail=f"Get Applicant Document with ID: {applicant_id} Failed")
    return document


@router.put("/submit/{applicant_id}")
def updated_applicant_status(applicant_id: str, db: Session = Depends(get_db)):
    applicant = crud.updated_applicant_status(db, applicant_id)
    if not applicant:
        raise HTTPException(status_code=404, detail=f"Updated Applicant Status with ID: {applicant_id} Failed")
    return applicant


@router.post("/refresh-token")
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    return perform_refresh_token(request, response, db)


@router.get("/get-admission-id/{appId}")
def get_admission_id(appId: str, db: Session = Depends(get_db), current_user: ApplicantGeneralInformation = Depends(get_current_user)):
    return crud.get_admission_id_by_app_id(db, appId)


@router.post("/updated-admission-id/{appId}/{admissionId}")
def updated_admission_id(
    appId: str,
    admissionId: str,
    db: Session = Depends(get_db),
    current_user: ApplicantGeneralInformation = Depends(get_current_user)
):
    return crud.updated_admission_id(db, appId, admissionId)


@router.get("/get-applicant-profile/{appId}")
def get_applicant_edit_info(
    appId: str,
    db: Session = Depends(get_db),
    current_user: ApplicantGeneralInformation = Depends(get_current_user)
):
    return crud.get_applicant_edited_profile(db, appId)


@router.put("/updated-applicant-profile/{appId}")
def edit_applicant_edit_info(
    appId: str,
    data: ApplicantEditProfile,
    db: Session = Depends(get_db),
    current_user: ApplicantGeneralInformation = Depends(get_current_user)
):
    return crud.updated_applicant_profile(db, appId, data)


