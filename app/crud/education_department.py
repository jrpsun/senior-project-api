from sqlalchemy.orm import Session
from app.models.education_department import EducationDepartment
from app.schemas.education_department import (
    EducationDepartmentCreate,
    EducationDepartmentUpdate,
)
from datetime import datetime


def create_education_department(db: Session, edu_data: EducationDepartmentCreate):
    new_edu = EducationDepartment(
        educationId=edu_data.educationId,
        prefix=edu_data.prefix,
        firstName=edu_data.firstName,
        lastName=edu_data.lastName,
        username=edu_data.username,
        password=edu_data.password,
        email=edu_data.email,
        phoneNumber=edu_data.phoneNumber,
        lastSeen=datetime.now().strftime("%d-%m-%Y %H.%M")
    )
    db.add(new_edu)
    db.commit()
    db.refresh(new_edu)
    return new_edu


def get_all_education_departments(db: Session):
    return db.query(EducationDepartment).all()


def get_education_department(db: Session, edu_id: str):
    return db.query(EducationDepartment).filter(EducationDepartment.educationId == edu_id).first()


def update_education_department(db: Session, edu_id: str, edu_data: EducationDepartmentUpdate):
    edu_record = db.query(EducationDepartment).filter(EducationDepartment.educationId == edu_id).first()
    if not edu_record:
        return None
    
    for key, value in edu_data.model_dump(exclude_unset=True).items():
        setattr(edu_record, key, value)

    db.commit()
    db.refresh(edu_record)
    return edu_record


def delete_education_department(db: Session, edu_id: str):
    edu_record = db.query(EducationDepartment).filter(EducationDepartment.educationId == edu_id).first()
    if edu_record:
        db.delete(edu_record)
        db.commit()
    return edu_record
