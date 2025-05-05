from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.schemas.applicant import *
from app.crud import applicant as crud
from app.services.auth import get_current_user, perform_refresh_token

router = APIRouter()


@router.get("/registrations/{applicantId}", response_model=ApplicantRegistrationsResponse)
def get_applicant_registrations_info(applicantId: str, db: Session = Depends(get_db)):
    return crud.get_applicant_info_registrations(db, applicantId)


@router.put("/general/{applicant_id}/{admissionId}")
def update_applicant_general_info(applicant_id: str, admissionId: str, update_data: ApplicantGeneralInformationUpdate, db: Session = Depends(get_db)):
    return crud.update_applicant_general_info(db, applicant_id, admissionId, update_data)


@router.get("/general/{applicant_id}/{admissionId}", response_model=ApplicantGeneralInformationResponse)
def get_applicant_general_info(applicant_id: str, admissionId: str, db: Session = Depends(get_db)):
    return crud.get_applicant_general_info(db, applicant_id, admissionId)


@router.put("/education/{applicant_id}/{admId}")
def update_applicant_education_info(applicant_id: str, admId: str, update_data: ApplicantEducationinfoUpdate, db: Session = Depends(get_db)):
    return crud.update_applicant_education_info(db, applicant_id, admId, update_data)


@router.get("/education/{applicant_id}/{admId}", response_model=ApplicantEducationInfoResponse)
def get_applicant_education_info(applicant_id: str, admId: str, db: Session = Depends(get_db)):
    return crud.get_applicant_education_info(db, applicant_id, admId)


@router.put("/reward")
def create_applicant_reward(update_data: list[ApplicantRewardResponse], db: Session = Depends(get_db)):
    return crud.process_applicant_rewards(db, update_data)


@router.get("/reward/{applicant_id}/{admId}", response_model=list[ApplicantRewardResponse])
def get_rewards_by_appId(applicant_id: str, admId: str, db: Session = Depends(get_db)):
    return crud.get_rewards_by_applicant_id(db, applicant_id, admId)


@router.delete("/reward/{reward_id}")
def delete_reward_by_id(reward_id: str, db: Session = Depends(get_db)):
    success = crud.delete_reward_by_id(db, reward_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Reward with id {reward_id} not found")
    return None


@router.put("/talent")
def created_or_updated_talent(updated_data: list[ApplicantTalentResponse], db: Session = Depends(get_db)):
    return crud.process_applicant_talents(db, updated_data)


@router.get("/talent/{applicant_id}/{admId}", response_model=list[ApplicantTalentResponse])
def get_talents_by_appId(applicant_id: str, admId: str, db: Session = Depends(get_db)):
    return crud.get_talents_by_applicant_id(db, applicant_id, admId)


@router.delete("/talent/{talent_id}")
def delete_talent_by_id(talent_id: str, db: Session = Depends(get_db)):
    success = crud.delete_talent_by_id(db, talent_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Talent with id {talent_id} not found")
    return None


@router.put("/training")
def created_or_updated_training(updated_data: list[ApplicantTrainingResponse], db: Session = Depends(get_db)):
    return crud.process_applicant_trainings(db, updated_data)


@router.get("/training/{applicant_id}/{admId}", response_model=list[ApplicantTrainingResponse])
def get_trining_by_appId(applicant_id: str, admId: str, db: Session = Depends(get_db)):
    return crud.get_trains_by_applicant_id(db, applicant_id, admId)


@router.delete("/training/{training_id}")
def delete_training_by_id(training_id: str, db: Session = Depends(get_db)):
    success = crud.delete_train_by_id(db, training_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Training with id {training_id} not found")
    return None


# Document
@router.put("/document/{applicant_id}/{admId}")
def updated_applicant_document(applicant_id: str, admId: str, updated_data: ApplicantDocumentsResponse, db: Session = Depends(get_db)):
    return crud.updated_applicant_document(db, applicant_id, admId, updated_data)


@router.get("/document/{applicant_id}/{admId}", response_model=ApplicantDocumentsResponse)
def get_applicant_document_by_id(applicant_id: str, admId: str, db: Session = Depends(get_db)):
    return crud.get_applicant_document(db, applicant_id, admId)


@router.put("/submit/{applicant_id}/{admId}")
def updated_applicant_status(applicant_id: str, admId: str, db: Session = Depends(get_db)):
    return crud.updated_applicant_status(db, applicant_id, admId)


@router.post("/refresh-token")
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    return perform_refresh_token(request, response, db)


@router.get("/get-admission-id/{appId}")
def get_admission_id(appId: str, db: Session = Depends(get_db)):
    return crud.get_admission_id_by_app_id(db, appId)


@router.post("/updated-admission-id/{appId}/{admissionId}")
def registration_applicant(
    appId: str,
    admissionId: str,
    db: Session = Depends(get_db)
):
    return crud.registration_applicant_to_admission(db, appId, admissionId)


@router.get("/get-applicant-profile/{appId}")
def get_applicant_edit_info(
    appId: str,
    db: Session = Depends(get_db)
):
    return crud.get_applicant_edited_profile(db, appId)


@router.put("/updated-applicant-profile/{appId}")
def edit_applicant_edit_info(
    appId: str,
    data: ApplicantEditProfile,
    db: Session = Depends(get_db)
):
    return crud.updated_applicant_profile(db, appId, data)


@router.get("/follow-status/{appId}")
def get_applicant_status(
    appId: str,
    db: Session = Depends(get_db)
):
    return crud.get_applicant_follow_status(db, appId)


@router.get("/{appId}/{admId}/is-complete")
def is_applicant_complete(
    appId: str,
    admId: str,
    db: Session = Depends(get_db)
):
    return crud.process_is_applicant_complete(db, appId, admId)


@router.get("/applicant-status/{appId}/{admId}")
def get_applicant_status(
    appId: str,
    admId: str,
    db: Session = Depends(get_db)
):
    return crud.process_get_applicant_status(db, appId, admId)


@router.put("/applicant-cancel")
def applicant_cancel(
    cancel_data: ApplicantCancel,
    db: Session = Depends(get_db)
):
    return crud.process_applicant_cancel(db, cancel_data)