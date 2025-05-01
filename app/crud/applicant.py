import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import *
from app.schemas.applicant import *
from app.services.auth import *
from typing import Optional
from datetime import timedelta
from fastapi import Response


# General Information
def update_applicant_general_info(db: Session, applicant_id: str, admissionId: str, update_data: ApplicantGeneralInformationUpdate):
    applicant = (db.query(ApplicantGeneralInformation)
                 .filter(ApplicantGeneralInformation.applicantId == applicant_id)
                 .filter(ApplicantGeneralInformation.programRegistered == admissionId)
                 .first())
    if not applicant:
        raise HTTPException(status_code=404, detail=f"Applicant with ID: {applicant_id} Not Found")

    update_dict = update_data.model_dump(exclude_unset=True)

    # # แปลง base64 เป็น binary data ถ้ามีรูปภาพ
    # field_list = ["applicantPicture", "docCopyIdCard", "docCopyPassport", "docCopyHouseRegis"]
    # for field in field_list:
    #     if field in update_dict and update_dict[field]:
    #         print("field", field)
    #         # เอา prefix "data:image/...;base64," ออกถ้ามี
    #         if ',' in update_dict[field]:
    #             update_dict[field] = update_dict[field].split(',')[1]
    

    models = [
        ApplicantGeneralInformation,
        ApplicantContact,
        ApplicantAddress,
        ApplicantContactPerson,
        ApplicantAdmissionChannel,
    ]

    updated_instances = []

    for model in models:
        instance = db.query(model).filter_by(applicantId=applicant_id, programRegistered=admissionId).first()
        for field, value in update_dict.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
        updated_instances.append(instance)

    db.commit()
    for instance in updated_instances:
        db.refresh(instance)
    
    return {"Message": f"Updated General Information Applicant id {applicant_id} Success."}


def get_applicant_general_info(db: Session, applicant_id: str, admissionId: str):
    query = (
        db.query(
            ApplicantGeneralInformation,
            ApplicantContact,
            ApplicantAddress,
            ApplicantContactPerson,
            ApplicantAdmissionChannel,
        )
        .outerjoin(ApplicantContact, ApplicantGeneralInformation.applicantId == ApplicantContact.applicantId)
        .outerjoin(ApplicantAddress, ApplicantGeneralInformation.applicantId == ApplicantAddress.applicantId)
        .outerjoin(ApplicantContactPerson, ApplicantGeneralInformation.applicantId == ApplicantContactPerson.applicantId)
        .outerjoin(ApplicantAdmissionChannel, ApplicantGeneralInformation.applicantId == ApplicantAdmissionChannel.applicantId)
        .filter(ApplicantGeneralInformation.applicantId == applicant_id)
        .filter(ApplicantGeneralInformation.programRegistered == admissionId)
        .first()
    )

    if not query:
        raise HTTPException(status_code=404, detail=f"Applicant with ID: {applicant_id} Not Found")

    general_info, contact, address, contact_person, admission_channel = query

    # ลบ _sa_instance_state และ applicantId ออกจาก dictionary
    general_info_dict = {k: v for k, v in general_info.__dict__.items() if k not in ('_sa_instance_state', 'applicantId', 'programRegistered')} if general_info else {}
    
    # ถ้ามีรูปภาพ ให้ส่งเป็น base64
    if hasattr(general_info, 'applicantPicture') and general_info.applicantPicture:
        general_info_dict['applicantPicture'] = general_info.applicantPicture

    address_dict = {k: v for k, v in address.__dict__.items() if k not in ('_sa_instance_state', 'applicantId', 'programRegistered')} if address else {}

    # รวมข้อมูลของ GeneralInfo และ AddressInfo
    general_info_with_address = GeneralInfoWithAddress(
        **general_info_dict,
        **address_dict,
        applicantId=applicant_id,
        programRegistered=admissionId
    )

    return ApplicantGeneralInformationResponse(
        general_info=general_info_with_address,
        contact_info=ContactInfo(**contact.__dict__) if contact else ContactInfo(),
        emergency_contact=EmergencyContact(**contact_person.__dict__) if contact_person else EmergencyContact(),
        admission_channel=AdmissionChannel(**admission_channel.__dict__) if admission_channel else AdmissionChannel(),
    )


# Education Information
def update_applicant_education_info(db: Session, applicant_id: str, admId: str, update_data: ApplicantEducationinfoUpdate):
    applicant = (db.query(ApplicantAcademicBackground)
                 .filter(ApplicantAcademicBackground.applicantId == applicant_id)
                 .filter(ApplicantAcademicBackground.programRegistered == admId)
                 .first())
    if not applicant:
        raise HTTPException(status_code=404, detail=f"Applicant with ID: {applicant_id} Not Found")

    update_dict = update_data.model_dump(exclude_unset=True)

    models = [
        ApplicantAcademicBackground,
        ApplicantEnglishExam,
        ApplicantMathematicsExam
    ]

    updated_instances = []

    for model in models:
        instance = db.query(model).filter_by(applicantId=applicant_id, programRegistered=admId).first()
        for field, value in update_dict.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
        updated_instances.append(instance)

    db.commit()
    for instance in updated_instances:
        db.refresh(instance)
    
    return {"Message": f"Updated Education Information Applicant id {applicant_id} Success."}


def get_applicant_education_info(db: Session, applicant_id: str, admId: str):
    query = (
        db.query(
            ApplicantAcademicBackground,
            ApplicantEnglishExam,
            ApplicantMathematicsExam
        )
        .outerjoin(ApplicantEnglishExam, ApplicantAcademicBackground.applicantId == ApplicantEnglishExam.applicantId)
        .outerjoin(ApplicantMathematicsExam, ApplicantAcademicBackground.applicantId == ApplicantMathematicsExam.applicantId)
        .filter(ApplicantAcademicBackground.applicantId == applicant_id)
        .filter(ApplicantAcademicBackground.programRegistered == admId)
        .first()
    )

    if not query:
        raise HTTPException(status_code=404, detail=f"Applicant with ID: {applicant_id} Not Found")
    
    academic, eng, math = query

    return ApplicantEducationInfoResponse(
        background=ApplicantEducationBackground(**academic.__dict__) if academic else ApplicantEducationBackground(),
        eng_exam=ApplicantEducationEngExam(**eng.__dict__) if eng else ApplicantEducationEngExam(),
        math_exam=ApplicantEducationMathExam(**math.__dict__) if math else ApplicantEducationMathExam(),
    )


# Award
def create_or_update_reward(db: Session, updated_data: ApplicantRewardResponse):
    db_reward = db.query(ApplicantReward).filter(ApplicantReward.rewardId == updated_data.rewardId).first()

    if db_reward:
        for key, value in updated_data.model_dump(exclude_unset=True).items():
            setattr(db_reward, key, value)
        
        db.commit()
        db.refresh(db_reward)

        return db_reward
        
    db_reward = ApplicantReward(
        rewardId=updated_data.rewardId if updated_data.rewardId is not None else "",
        applicantId=updated_data.applicantId if updated_data.applicantId is not None else "",
        programRegistered=updated_data.programRegistered if updated_data.programRegistered is not None else "",
        nameOfCompetition=updated_data.nameOfCompetition if updated_data.nameOfCompetition is not None else "",
        rewardYear=updated_data.rewardYear if updated_data.rewardYear is not None else "",
        rewardLevel=updated_data.rewardLevel if updated_data.rewardLevel is not None else "",
        rewardAwards=updated_data.rewardAwards if updated_data.rewardAwards is not None else "",
        project=updated_data.project if updated_data.project is not None else "",
        rewardCer=updated_data.rewardCer if updated_data.rewardCer is not None else "",
        rewardCerName=updated_data.rewardCerName if updated_data.rewardCerName is not None else "",
        rewardCerSize=updated_data.rewardCerSize if updated_data.rewardCerSize is not None else ""
    )

    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)

    return db_reward
    

def process_applicant_rewards(db: Session, rewards: list[ApplicantRewardResponse]):
    results = []
    for reward in rewards:
        results.append(create_or_update_reward(db, reward))
    
    return results


def get_rewards_by_applicant_id(db: Session, applicant_id: str, admId: str):
    rewards = (db.query(ApplicantReward)
               .filter(ApplicantReward.applicantId == applicant_id)
               .filter(ApplicantReward.programRegistered == admId)
               .all()
            )
    
    if not rewards:
        return []
    
    return rewards


def delete_reward_by_id(db: Session, reward_id: str):
    try:
        db_reward = db.query(ApplicantReward).filter(ApplicantReward.rewardId == reward_id).first()

        if not db_reward:
            return False
        
        db.delete(db_reward)
        db.commit()
        
        return True
    except Exception as e:
        db.rollback()
        raise e
    

# Talent
def create_or_update_talent(db: Session, updated_data: ApplicantTalentResponse):
    db_talent = db.query(ApplicantTalent).filter(ApplicantTalent.talentId == updated_data.talentId).first()

    if db_talent:
        for key, value in updated_data.model_dump(exclude_unset=True).items():
            setattr(db_talent, key, value)
        
        db.commit()
        db.refresh(db_talent)

        return db_talent

    db_talent = ApplicantTalent(
        talentId=updated_data.talentId if updated_data.talentId is not None else "",
        applicantId = updated_data.applicantId if updated_data.applicantId is not None else "",
        programRegistered = updated_data.programRegistered if updated_data.programRegistered is not None else "",
        kindOfTalent = updated_data.kindOfTalent if updated_data.kindOfTalent is not None else "",
        nameOfCompetition = updated_data.nameOfCompetition if updated_data.nameOfCompetition is not None else "",
        talentYear = updated_data.talentYear if updated_data.talentYear is not None else "",
        talentAwards = updated_data.talentAwards if updated_data.talentAwards is not None else "",
        url = updated_data.url if updated_data.url is not None else "",
        moreDetails = updated_data.moreDetails if updated_data.moreDetails is not None else "",
        talentCer = updated_data.talentCer if updated_data.talentCer is not None else "",
        talentCerName = updated_data.talentCerName if updated_data.talentCerName is not None else "",
        talentCerSize = updated_data.talentCerSize if updated_data.talentCerSize is not None else ""
    )

    db.add(db_talent)
    db.commit()
    db.refresh(db_talent)

    return db_talent


def process_applicant_talents(db: Session, talents: list[ApplicantTalentResponse]):
    results = []
    for talent in talents:
        results.append(create_or_update_talent(db, talent))
    
    return results


def get_talents_by_applicant_id(db: Session, applicant_id: str, admId: str):
    talents = (db.query(ApplicantTalent)
               .filter(ApplicantTalent.applicantId == applicant_id)
               .filter(ApplicantTalent.programRegistered == admId)
               .all()
            )
    
    if not talents:
        return []
    
    return talents


def delete_talent_by_id(db: Session, talent_id: str):
    try:
        db_talent = db.query(ApplicantTalent).filter(ApplicantTalent.talentId == talent_id).first()

        if not db_talent:
            return False
        
        db.delete(db_talent)
        db.commit()
        
        return True
    except Exception as e:
        db.rollback()
        raise e


# Training
def create_or_update_training(db: Session, updated_data: ApplicantTrainingResponse):
    db_training = db.query(ApplicantTraining).filter(ApplicantTraining.trainingId == updated_data.trainingId).first()

    if db_training:
        for key, value in updated_data.model_dump(exclude_unset=True).items():
            setattr(db_training, key, value)
        
        db.commit()
        db.refresh(db_training)

        return db_training
    
    db_training = ApplicantTraining(
        trainingId = updated_data.trainingId if updated_data.trainingId is not None else "",
        applicantId = updated_data.applicantId if updated_data.applicantId is not None else "",
        programRegistered = updated_data.programRegistered if updated_data.programRegistered is not None else "",
        nameOfCourse = updated_data.nameOfCourse if updated_data.nameOfCourse is not None else "",
        institution = updated_data.institution if updated_data.institution is not None else "",
        trainingYear =  updated_data.trainingYear if updated_data.trainingYear is not None else "",
        trainingMode = updated_data.trainingMode if updated_data.trainingMode is not None else "",
        trainingCountry = updated_data.trainingCountry if updated_data.trainingCountry is not None else "",
        trainingCer = updated_data.trainingCer if updated_data.trainingCer is not None else "",
        trainingCerName = updated_data.trainingCerName if updated_data.trainingCerName is not None else "",
        trainingCerSize = updated_data.trainingCerSize if updated_data.trainingCerSize is not None else ""
    )

    db.add(db_training)
    db.commit()
    db.refresh(db_training)

    return db_training


def process_applicant_trainings(db: Session, trains: list[ApplicantTalentResponse]):
    results = []
    for train in trains:
        results.append(create_or_update_training(db, train))
    
    return results


def get_trains_by_applicant_id(db: Session, applicant_id: str, admId: str):
    trains = (db.query(ApplicantTraining)
              .filter(ApplicantTraining.applicantId == applicant_id)
              .filter(ApplicantTraining.programRegistered == admId)
              .all()
            )
    
    if not trains:
        return []
    
    return trains


def delete_train_by_id(db: Session, training_id: str):
    try:
        db_train = db.query(ApplicantTraining).filter(ApplicantTraining.trainingId == training_id).first()

        if not db_train:
            return False
        
        db.delete(db_train)
        db.commit()
        
        return True
    except Exception as e:
        db.rollback()
        raise e
    

# Document
def updated_applicant_document(db: Session, appId: str, admId: str, updated_data: ApplicantDocumentsResponse):
    applicant = (db.query(ApplicantAdditionalDocuments)
                 .filter(ApplicantAdditionalDocuments.applicantId == appId)
                 .filter(ApplicantAdditionalDocuments.programRegistered == admId)
                 .first()
                )

    if not applicant:
        raise HTTPException(status_code=404, detail=f"Updated Applicant Document with ID: {appId} Failed")

    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(applicant, key, value)
    
    db.commit()
    db.refresh(applicant)

    return applicant


def get_applicant_document(db: Session, appId: str, admId: str):
    document = (db.query(ApplicantAdditionalDocuments)
                .filter(ApplicantAdditionalDocuments.applicantId == appId)
                .filter(ApplicantAdditionalDocuments.programRegistered == admId)
                .first()
            )
    
    if not document:
        raise HTTPException(status_code=404, detail=f"Applicant Document with ID: {appId} not found")
    
    return document


# Submit
def updated_applicant_status(db: Session, appId: str, admId: str):
    applicant = (db.query(ApplicantStatus)
                 .filter(ApplicantStatus.applicantId == appId)
                 .filter(ApplicantStatus.programRegistered == admId)
                 .first()
                )

    if not applicant:
        raise HTTPException(status_code=404, detail=f"Applicant with ID: {appId} not found")


    if applicant:
        applicant.admissionStatus = "02 - ยื่นใบสมัครแล้ว"
        applicant.paymentStatus = "03 - ชำระเงินเรียบร้อย"
        applicant.docStatus = "02 - รอตรวจสอบเอกสาร"

        db.commit()
        db.refresh(applicant)

    return applicant


def get_admission_id_by_app_id(db: Session, appId: str):
    applicant = db.query(ApplicantGeneralInformation).filter(ApplicantGeneralInformation.applicantId == appId).first()

    if not applicant:
        raise HTTPException(status_code=404, detail=f"Applicant with ID: {appId} Not Found")
    
    if not applicant.programRegistered:
        return ""

    return applicant.programRegistered


def registration_applicant_to_admission(db: Session, appId: str, admissionId: str):
    if not db.query(ApplicantRegistrations).filter(ApplicantRegistrations.applicantId == appId).first():
        raise HTTPException(status_code=404, detail=f"Applicant with ID: {appId} Not Found")
    
    if (db.query(ApplicantGeneralInformation)
        .filter(ApplicantGeneralInformation.applicantId == appId)
        .filter(ApplicantGeneralInformation.programRegistered == admissionId)
        .first()
    ):
        raise HTTPException(status_code=409, detail=f"Applicant with ID: {appId} already registered in program {admissionId}")

    applicant_models = [
        ApplicantContact,
        ApplicantAddress,
        ApplicantContactPerson,
        ApplicantAdmissionChannel,
        ApplicantEnglishExam,
        ApplicantAcademicBackground,
        ApplicantMathematicsExam,
        ApplicantAdditionalDocuments,
        PreliminaryEvaluation
    ]

    new_records = [model(applicantId=appId, programRegistered=admissionId) for model in applicant_models]
    db.add_all(new_records)
    db.commit()

    new_applicant_number = ApplicantGeneralInformation(
        applicantId=appId,
        programRegistered=admissionId,
        applicant_number = generate_app_index(db, admissionId)
    )
    db.add(new_applicant_number)
    db.commit()

    new_applicant_status = ApplicantStatus(
        applicantId=appId,
        programRegistered=admissionId,
        admissionStatus="01 - ยังไม่ยื่นใบสมัคร",
        paymentStatus="01 - ยังไม่ได้ชำระเงิน",
        docStatus="01 - ยังไม่มีเอกสาร"
    )

    db.add(new_applicant_status)
    db.commit()

    for record in new_records:
        db.refresh(record)

    db.refresh(new_applicant_number)

    return {"Message": f"Created applicant with ID: {appId} in registered program {admissionId} success"}


def generate_app_index(db: Session, admissionId: str):
    last_user = (db.query(ApplicantGeneralInformation)
                 .filter(ApplicantGeneralInformation.programRegistered == admissionId)
                 .order_by(ApplicantGeneralInformation.applicant_number.desc())
                 .first())
    
    if not last_user or not last_user.applicant_number:
        return "0000001"
    last_id = int(last_user.applicant_number)
    next_id = last_id + 1
    return str(next_id).zfill(7)


def get_applicant_edited_profile(db: Session, appId: str):
    applicant = db.query(ApplicantRegistrations).filter(ApplicantRegistrations.applicantId == appId).first()

    if not applicant:
        raise HTTPException(status_code=404, detail=f"Applicant with ID: {appId} Not Found")

    return applicant


def updated_applicant_profile(db: Session, appId: str, data: ApplicantEditProfile):
    applicant = db.query(ApplicantRegistrations).filter(ApplicantRegistrations.applicantId == appId).first()

    if not applicant:
        raise HTTPException(status_code=404, detail=f"Applicant with ID: {appId} Not Found")
    
    applicant.prefix = data.prefix
    applicant.firstnameTH = data.firstNameTH
    applicant.lastnameTH = data.lastNameTH
    applicant.firstnameEN = data.firstNameEN
    applicant.lastnameEN = data.lastNameEN
    applicant.applicantEmail = data.email

    db.commit()
    db.refresh(applicant)

    return applicant


def get_applicant_info_registrations(db: Session, appId: str) -> ApplicantRegistrationsResponse:
    applicant = db.query(ApplicantRegistrations).filter(ApplicantRegistrations.applicantId == appId).first()

    if not applicant:
        raise HTTPException(status_code=404, detail=f"Applicant with ID: {appId} Not Found")
    
    return applicant

