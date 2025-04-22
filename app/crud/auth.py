import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import *
from app.schemas.auth import *
from app.services.auth import *
from typing import Optional
from datetime import timedelta
from fastapi import Response


def create_applicant(db: Session, applicant_data: ApplicantCreate):
    new_applicant_id = generate_next_id(db)

    new_applicant_general = ApplicantGeneralInformation(
        applicantId=new_applicant_id,
        nationality=applicant_data.nationality,
        idCardNumber=applicant_data.idNumber if applicant_data.idType == "citizen" else "",
        passportId=applicant_data.idNumber if applicant_data.idType == "passport" else "",
        prefix=applicant_data.title,
        firstnameTH=applicant_data.firstNameThai,
        lastnameTH=applicant_data.lastNameThai,
        firstnameEN=applicant_data.firstNameEnglish,
        lastnameEN=applicant_data.lastNameEnglish,
        submissionStatus=False,
        password=hash_password(applicant_data.password),
    )

    new_contact = ApplicantContact(
        applicantId=new_applicant_id,
        applicantEmail=applicant_data.email,
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
        PreliminaryEvaluation
    ]

    new_records = [model(applicantId=new_applicant_id) for model in applicant_models]
    
    db.add(new_applicant_general)
    db.commit()

    db.add(new_contact)
    db.add_all(new_records)
    db.commit()

    db.refresh(new_applicant_general)
    db.refresh(new_contact)
    for record in new_records:
        db.refresh(record)

    return {"Message": f"Create Applicant id {new_applicant_id} Success."}


def generate_next_id(db: Session) -> str:
    last_user = db.query(ApplicantGeneralInformation).order_by(ApplicantGeneralInformation.applicantId.desc()).first()
    if not last_user:
        return "0000001"
    last_id = int(last_user.applicantId)
    next_id = last_id + 1
    return str(next_id).zfill(7)



def applicant_login(response: Response, db: Session, idNumber: str, password: str):
    user: Optional[ApplicantGeneralInformation] = db.query(ApplicantGeneralInformation).filter(
        (ApplicantGeneralInformation.idCardNumber == idNumber) |
        (ApplicantGeneralInformation.passportId == idNumber)
    ).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token(
        data={"sub": user.firstnameEN + " " + user.lastnameEN, "appId": user.applicantId},
        expires_delta=timedelta(minutes=60)
    )

    refresh_token = create_token(
        data={"sub": user.firstnameEN, "appId": user.applicantId},
        expires_delta=timedelta(days=1),
        secret=REFRESH_SECRET
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


def admin_login(response: Response, db: Session, email: str, password: str):
    roles = []
    name = ""
    user_id = None

    def check_role(model, role_name, role_field):
        nonlocal name, user_id
        user = db.query(model).filter(model.email == email).first()
        # if user and verify_password(password, user.password): TODO Hashed code
        if user and password == user.password:
            roles.append(role_name)
            name = f"{user.firstName} {user.lastName}"
            user_id = getattr(user, role_field)
        return user

    check_role(EducationDepartment, "education_department", "educationId")
    check_role(InterviewCommittee, "interview", "interviewComId")
    check_role(CourseCommittee, "course_committee", "courseComId")
    check_role(PublicRelations, "public_relations", "PRid")

    if not roles:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token(
        data={"sub": name, "id": user_id, "email": email, "roles": roles},
        expires_delta=timedelta(minutes=60)
    )

    refresh_token = create_token(
        data={"sub": name, "id": user_id, "email": email, "roles": roles},
        expires_delta=timedelta(days=1)
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }




    