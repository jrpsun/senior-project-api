from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import *
from app.schemas.applicant import (
    ApplicantCreate,
    ApplicantGeneralInformationUpdate,
    ApplicantGeneralInformationResponse,
)


def create_applicant(db: Session, applicant_data: ApplicantCreate):
    ## TODO programRegistered 
    ## TODO encrypt password

    new_applicant_general = ApplicantGeneralInformation(
        applicantId=applicant_data.applicantId,
        nationality=applicant_data.nationality,
        idCardNumber=applicant_data.idCardNumber,
        passportId=applicant_data.passportId,
        prefix=applicant_data.prefix,
        firstnameTH=applicant_data.firstnameTH,
        lastnameTH=applicant_data.lastnameTH,
        firstnameEN=applicant_data.firstnameEN,
        lastnameEN=applicant_data.lastnameEN,
        submissionStatus=False,
        password=applicant_data.password,
    )

    new_contact = ApplicantContact(
        applicantId=applicant_data.applicantId,
        email=applicant_data.email,
    )

    applicant_models = [
        ApplicantAddress,
        ApplicantContactPerson,
        ApplicantAdmissionChannel,
        ApplicantEnglishExam,
        ApplicantAcademicBackground,
        ApplicantMathematicsExam,
        ApplicantAdditionalDocuments,
        ApplicantStatus,
    ]

    new_records = [model(applicantId=applicant_data.applicantId) for model in applicant_models]
    
    db.add(new_applicant_general)
    db.commit()

    db.add(new_contact)
    db.add_all(new_records)
    db.commit()

    db.refresh(new_applicant_general)
    db.refresh(new_contact)
    for record in new_records:
        db.refresh(record)

    return {"Message": f"Create Applicant id {applicant_data.applicantId} Success."}


def update_applicant_general_info(db: Session, applicant_id: str, update_data: ApplicantGeneralInformationUpdate):
    applicant = db.query(ApplicantGeneralInformation).filter_by(applicantId=applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    update_dict = update_data.model_dump(exclude_unset=True)

    models = [
        ApplicantGeneralInformation,
        ApplicantContact,
        ApplicantAddress,
        ApplicantContactPerson,
        ApplicantAdmissionChannel,
    ]

    updated_instances = []

    for model in models:
        instance = db.query(model).filter_by(applicantId=applicant_id).first()
        for field, value in update_dict.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
        updated_instances.append(instance)

    db.commit()
    for instance in updated_instances:
        db.refresh(instance)
    
    return {"Message": f"Updated Applicant id {applicant_id} Success."}


def get_applicant_general_info(db: Session, applicant_id: str):
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
        .first()
    )

    if not query:
        return {"Message": "Applicant not found"}

    general_info, contact, address, contact_person, admission_channel = query

    response_data = {}

    if general_info:
        response_data.update(general_info.__dict__)

    if contact:
        response_data.update(contact.__dict__)

    if address:
        response_data.update(address.__dict__)

    if contact_person:
        response_data.update(contact_person.__dict__)

    if admission_channel:
        response_data.update(admission_channel.__dict__)

    response_data.pop("_sa_instance_state", None)

    return ApplicantGeneralInformationResponse(**response_data).model_dump(exclude_unset=True)


