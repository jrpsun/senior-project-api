from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import *
from app.schemas.excel import ApplicantFilterCourseSummary, ApplicantFilterExcel


def get_applicant_list(db: Session, admissionId: str, filter_data: ApplicantFilterExcel):
    query = (
        db.query(
            ApplicantGeneralInformation,
            ApplicantAcademicBackground,
            ApplicantStatus,
            ApplicantContact,
            ApplicantRegistrations
        )
        .outerjoin(
            ApplicantAcademicBackground,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantAcademicBackground.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantAcademicBackground.programRegistered
            )
        )
        .outerjoin(
            ApplicantStatus,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantStatus.programRegistered
            )
        )
        .outerjoin(
            ApplicantContact,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantContact.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantContact.programRegistered
            )
        )
        .outerjoin(
            ApplicantRegistrations, ApplicantGeneralInformation.applicantId == ApplicantRegistrations.applicantId
        )
        .filter(ApplicantGeneralInformation.programRegistered == admissionId)
    )

    if filter_data.admitStatus:
        query = query.filter(ApplicantStatus.admissionStatus == filter_data.admitStatus)
    
    if filter_data.docStatus:
        query = query.filter(ApplicantStatus.docStatus == filter_data.docStatus)

    if filter_data.paymentStatus:
        query = query.filter(ApplicantStatus.paymentStatus == filter_data.paymentStatus)

    applicant = query.all()

    result = []
    for g, a, s, c, r in applicant:
        item = {
            "applicantId": g.applicantId,
            "name": f"{r.firstnameTH if r.firstnameTH else r.firstnameEN} {r.lastnameTH if r.lastnameTH else r.lastnameEN}",
            "school": a.schoolName,
            "cgpa": a.cumulativeGPA,
            "dst_m": a.dstMathematics,
            "dst_e": a.dstEnglish,
            "dst_s": a.dstScitech,
            "admissionStatus": s.admissionStatus,
            "docStatus": s.docStatus,
            "paymentStatus": s.paymentStatus,
            "email": r.applicantEmail,
            "phone": c.applicantPhone,
            "applyDate": s.applyDate
        }

        result.append(item)


    return result


def get_admission_by_filter_data(db: Session, filter_data: ApplicantFilterExcel):
    admission = db.query(Admission).filter_by(
        program=filter_data.course,
        roundName=filter_data.round,
        academicYear=filter_data.year
    ).first()

    if not admission:
        raise HTTPException(status_code=404, detail=f"Admission Not Found")

    return admission


def get_applicant_screening_group(db: Session, admissionId: str, filter_data: ApplicantFilterExcel):
    query = (
        db.query(
            ApplicantGeneralInformation,
            ApplicantAcademicBackground,
            ApplicantStatus,
            ApplicantContact,
            PreliminaryEvaluation,
            CourseCommittee,
            Admission,
            ApplicantRegistrations
        )
        .outerjoin(
            ApplicantAcademicBackground,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantAcademicBackground.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantAcademicBackground.programRegistered
            )
        )
        .outerjoin(
            ApplicantStatus,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantStatus.programRegistered
            )
        )
        .outerjoin(
            ApplicantContact,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantContact.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantContact.programRegistered
            )
        )
        .outerjoin(
            PreliminaryEvaluation,
            and_(
                ApplicantGeneralInformation.applicantId == PreliminaryEvaluation.applicantId,
                ApplicantGeneralInformation.programRegistered == PreliminaryEvaluation.programRegistered
            )
        )
        .outerjoin(
            CourseCommittee, PreliminaryEvaluation.courseComId == CourseCommittee.courseComId
        )
        .outerjoin(
            Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId
        )
        .outerjoin(
            ApplicantRegistrations, ApplicantGeneralInformation.applicantId == ApplicantRegistrations.applicantId
        )
        .filter(ApplicantGeneralInformation.programRegistered == admissionId)
    )

    if filter_data.admitStatus:
        query = query.filter(ApplicantStatus.admissionStatus == filter_data.admitStatus)
    
    if filter_data.docStatus:
        query = query.filter(ApplicantStatus.docStatus == filter_data.docStatus)

    if filter_data.paymentStatus:
        query = query.filter(ApplicantStatus.paymentStatus == filter_data.paymentStatus)

    applicant = query.all()

    result = []
    for general, academic, status, contact, pre, cc, adm, regis in applicant:
        item = {
            "course": adm.program,
            "round": adm.roundName,
            "applicantNumber": general.applicant_number,
            "name": f"{regis.firstnameTH if regis.firstnameTH else regis.firstnameEN} {regis.lastnameTH if regis.lastnameTH else regis.lastnameEN}",
            "school": academic.schoolName,
            "admissionStatus": status.admissionStatus,
            "docStatus": status.docStatus,
            "paymentStatus": status.paymentStatus,
            "email": regis.applicantEmail,
            "phone": contact.applicantPhone,
            "ccName": f"{cc.firstName} {cc.lastName}"
        }

        result.append(item)


    return result


def get_applicant_screening_summary(db: Session, filter_data: ApplicantFilterCourseSummary):
    admission = db.query(Admission).filter_by(
        program=filter_data.course,
        roundName=filter_data.round,
        academicYear=filter_data.year
    ).first()

    if not admission:
        raise HTTPException(status_code=404, detail=f"Admission Not Found")
    
    query = (
        db.query(
            ApplicantGeneralInformation,
            ApplicantAcademicBackground,
            ApplicantStatus,
            ApplicantContact,
            PreliminaryEvaluation,
            CourseCommittee,
            Admission,
            ApplicantRegistrations
        )
        .outerjoin(
            ApplicantAcademicBackground,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantAcademicBackground.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantAcademicBackground.programRegistered
            )
        )
        .outerjoin(
            ApplicantStatus,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantStatus.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantStatus.programRegistered
            )
        )
        .outerjoin(
            ApplicantContact,
            and_(
                ApplicantGeneralInformation.applicantId == ApplicantContact.applicantId,
                ApplicantGeneralInformation.programRegistered == ApplicantContact.programRegistered
            )
        )
        .outerjoin(
            PreliminaryEvaluation,
            and_(
                ApplicantGeneralInformation.applicantId == PreliminaryEvaluation.applicantId,
                ApplicantGeneralInformation.programRegistered == PreliminaryEvaluation.programRegistered
            )
        )
        .outerjoin(
            CourseCommittee, PreliminaryEvaluation.courseComId == CourseCommittee.courseComId
        )
        .outerjoin(
            Admission, ApplicantGeneralInformation.programRegistered == Admission.admissionId
        )
        .outerjoin(
            ApplicantRegistrations, ApplicantGeneralInformation.applicantId == ApplicantRegistrations.applicantId
        )
        .filter(ApplicantGeneralInformation.programRegistered == admission.admissionId)
    )

    if filter_data.admitStatus:
        query = query.filter(ApplicantStatus.admissionStatus == filter_data.admitStatus)
    
    if filter_data.docStatus:
        query = query.filter(ApplicantStatus.docStatus == filter_data.docStatus)

    if filter_data.paymentStatus:
        query = query.filter(ApplicantStatus.paymentStatus == filter_data.paymentStatus)

    applicant = query.all()

    result = []
    for general, academic, status, contact, pre, cc, adm, regis in applicant:
        item = {
            "course": adm.program,
            "round": adm.roundName,
            "applicantNumber": general.applicant_number,
            "name": f"{regis.firstnameTH if regis.firstnameTH else regis.firstnameEN} {regis.lastnameTH if regis.lastnameTH else regis.lastnameEN}",
            "school": academic.schoolName,
            "cgpa": academic.cumulativeGPA,
            "dst_m": academic.dstMathematics,
            "dst_e": academic.dstEnglish,
            "dst_s": academic.dstScitech,
            "admissionStatus": status.admissionStatus,
            "docStatus": status.docStatus,
            "email": regis.applicantEmail,
            "phone": contact.applicantPhone,
            "ccName": f"{cc.firstName} {cc.lastName}",
            "comment": pre.preliminaryComment,
            "date": f"{pre.preEvaDate if pre.preEvaDate else "รอการประเมิน"}"
        }

        result.append(item)


    return result