from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import *
from app.schemas.applicant import (
    AdmissionChannel,
    ApplicantCreate,
    ApplicantGeneralInformationUpdate,
    ApplicantGeneralInformationResponse,
    ApplicantEducationinfoUpdate,
    ApplicantEducationInfoResponse,
    ApplicantAdminDashboardResponse,
    ApplicantListAdminDashboardResponse,
    ContactInfo,
    EmergencyContact,
    GeneralInfoWithAddress,
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
        applicantEmail=applicant_data.applicantEmail,
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


# General Information
def update_applicant_general_info(db: Session, applicant_id: str, update_data: ApplicantGeneralInformationUpdate):
    applicant = db.query(ApplicantGeneralInformation).filter_by(applicantId=applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    update_dict = update_data.model_dump(exclude_unset=True)

    # แปลง base64 เป็น binary data ถ้ามีรูปภาพ
    if 'applicantPicture' in update_dict and update_dict['applicantPicture']:
        # เอา prefix "data:image/...;base64," ออกถ้ามี
        if ',' in update_dict['applicantPicture']:
            update_dict['applicantPicture'] = update_dict['applicantPicture'].split(',')[1]

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
    
    return {"Message": f"Updated General Information Applicant id {applicant_id} Success."}


# def get_applicant_general_info(db: Session, applicant_id: str):
#     query = (
#         db.query(
#             ApplicantGeneralInformation,
#             ApplicantContact,
#             ApplicantAddress,
#             ApplicantContactPerson,
#             ApplicantAdmissionChannel,
#         )
#         .outerjoin(ApplicantContact, ApplicantGeneralInformation.applicantId == ApplicantContact.applicantId)
#         .outerjoin(ApplicantAddress, ApplicantGeneralInformation.applicantId == ApplicantAddress.applicantId)
#         .outerjoin(ApplicantContactPerson, ApplicantGeneralInformation.applicantId == ApplicantContactPerson.applicantId)
#         .outerjoin(ApplicantAdmissionChannel, ApplicantGeneralInformation.applicantId == ApplicantAdmissionChannel.applicantId)
#         .filter(ApplicantGeneralInformation.applicantId == applicant_id)
#         .first()
#     )

#     if not query:
#         return {"Message": "Applicant not found"}

#     general_info, contact, address, contact_person, admission_channel = query

#     response_data = {}

#     if general_info:
#         response_data.update(general_info.__dict__)

#     if contact:
#         response_data.update(contact.__dict__)

#     if address:
#         response_data.update(address.__dict__)

#     if contact_person:
#         response_data.update(contact_person.__dict__)

#     if admission_channel:
#         response_data.update(admission_channel.__dict__)

#     response_data.pop("_sa_instance_state", None)

#     return ApplicantGeneralInformationResponse(**response_data).model_dump(exclude_unset=True)


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
        return None

    general_info, contact, address, contact_person, admission_channel = query

    # ลบ _sa_instance_state และ applicantId ออกจาก dictionary
    general_info_dict = {k: v for k, v in general_info.__dict__.items() if k not in ('_sa_instance_state', 'applicantId')} if general_info else {}
    
    # ถ้ามีรูปภาพ ให้ส่งเป็น base64
    if hasattr(general_info, 'applicantPicture') and general_info.applicantPicture:
        general_info_dict['applicantPicture'] = general_info.applicantPicture

    address_dict = {k: v for k, v in address.__dict__.items() if k not in ('_sa_instance_state', 'applicantId')} if address else {}

    # รวมข้อมูลของ GeneralInfo และ AddressInfo
    general_info_with_address = GeneralInfoWithAddress(
        **general_info_dict,
        **address_dict,
        applicantId=applicant_id  # ส่ง applicantId แยกต่างหาก
    )

    return ApplicantGeneralInformationResponse(
        general_info=general_info_with_address,
        contact_info=ContactInfo(**contact.__dict__) if contact else ContactInfo(),
        emergency_contact=EmergencyContact(**contact_person.__dict__) if contact_person else EmergencyContact(),
        admission_channel=AdmissionChannel(**admission_channel.__dict__) if admission_channel else AdmissionChannel(),
    )


# Education Information
def update_applicant_education_info(db: Session, applicant_id: str, update_data: ApplicantEducationinfoUpdate):
    applicant = db.query(ApplicantGeneralInformation).filter_by(applicantId=applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    update_dict = update_data.model_dump(exclude_unset=True)

    models = [
        ApplicantAcademicBackground,
        ApplicantEnglishExam,
        ApplicantMathematicsExam
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
    
    return {"Message": f"Updated Education Information Applicant id {applicant_id} Success."}


def get_applicant_education_info(db: Session, applicant_id: str):
    query = (
        db.query(
            ApplicantAcademicBackground,
            ApplicantEnglishExam,
            ApplicantMathematicsExam
        )
        .outerjoin(ApplicantEnglishExam, ApplicantAcademicBackground.applicantId == ApplicantEnglishExam.applicantId)
        .outerjoin(ApplicantMathematicsExam, ApplicantAcademicBackground.applicantId == ApplicantMathematicsExam.applicantId)
        .filter(ApplicantAcademicBackground.applicantId == applicant_id)
        .first()
    )

    if not query:
        return {"Message": "Applicant not found"}
    
    academic, eng, math = query

    response_data = {}

    if academic:
        response_data.update(academic.__dict__)

    if eng:
        response_data.update(eng.__dict__)
        
    if math:
        response_data.update(math.__dict__)
    
    response_data.pop("_sa_instance_state", None)
    
    return ApplicantEducationInfoResponse(**response_data).model_dump(exclude_unset=True)


# DashBoard Admin
def get_all_applicant_for_admin_dashboard(db: Session):
    query = (
        db.query(
            ApplicantGeneralInformation,
            ApplicantContact,
            ApplicantStatus,
            Admission
        )
        .outerjoin(ApplicantContact, ApplicantGeneralInformation.applicantId == ApplicantContact.applicantId)
        .outerjoin(ApplicantStatus, ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId)
        .outerjoin(Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId)
    ).all()

    if not query:
        return {"Message": "Applicant not found"}
    
    response_list = []
    for general, contact, status, admit in query:
        response_data = {}

        if general:
            response_data.update(general.__dict__)

        if contact:
            response_data.update(contact.__dict__)

        if status:
            response_data.update(status.__dict__)

        if admit:
            response_data.update(admit.__dict__)

        response_list.append(ApplicantAdminDashboardResponse(**response_data).model_dump(exclude_unset=True))

    return ApplicantListAdminDashboardResponse(applicants=response_list)


    
