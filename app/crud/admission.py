from sqlalchemy.orm import Session
from app.models.admission import Admission
from app.schemas.admission import (
    AdmissionBase,
    AdmissionUpdate
)


def create_admission(db: Session, admission_data: AdmissionBase):
    new_admission = Admission(
        admissionId=admission_data.admissionId,
        program=admission_data.program,
        roundName=admission_data.roundName,
        academicYear=admission_data.academicYear,
        startDate=admission_data.startDate,
        endDate=admission_data.endDate
    )
    db.add(new_admission)
    db.commit()
    db.refresh(new_admission)
    return new_admission


def get_all_admissions(db: Session):
    return db.query(Admission).all()


def get_admission(db: Session, admission_id: str):
    return db.query(Admission).filter(Admission.admissionId == admission_id).first()


def update_admission(db: Session, admission_id: str, admission_data: AdmissionUpdate):
    admission_record = db.query(Admission).filter(Admission.admissionId == admission_id).first()
    if not admission_record:
        return None
    
    for key, value in admission_data.model_dump(exclude_unset=True).items():
        setattr(admission_record, key, value)

    db.commit()
    db.refresh(admission_record)
    return admission_record


def delete_admission(db: Session, admission_id: str):
    admission_record = db.query(Admission).filter(Admission.admissionId == admission_id).first()
    if admission_record:
        db.delete(admission_record)
        db.commit()
    return admission_record