from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import *


def get_applicant_list(db: Session, admissionId: str):
    raw_data = (
        db.query(
            ApplicantGeneralInformation,
            ApplicantAcademicBackground,
            ApplicantStatus,
            ApplicantContact,
        )
        .outerjoin(ApplicantAcademicBackground, ApplicantGeneralInformation.applicantId == ApplicantAcademicBackground.applicantId)
        .outerjoin(ApplicantStatus, ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId)
        .outerjoin(ApplicantContact, ApplicantGeneralInformation.applicantId == ApplicantContact.applicantId)
        .filter(ApplicantGeneralInformation.programRegistered == admissionId)
        .all()
    )

    result = []
    for g, a, s, c in raw_data:
        item = {
            "applicantId": g.applicantId,
            "name": g.firstnameEN + " " + g.lastnameEN,
            "school": a.schoolName,
            "cgpa": a.cumulativeGPA,
            "dst_m": a.dstMathematics,
            "dst_e": a.dstEnglish,
            "dst_s": a.dstScitech,
            "admissionStatus": s.admissionStatus,
            "docStatus": s.docStatus,
            "paymentStatus": s.paymentStatus,
            "email": c.applicantEmail,
            "phone": c.applicantPhone,
            "applyDate": s.applyDate
        }

        result.append(item)


    return result


def get_admission_by_id(db: Session, admissionId: str):
    return db.query(Admission).filter(Admission.admissionId == admissionId).first()