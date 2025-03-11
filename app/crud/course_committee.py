from sqlalchemy.orm import Session
from app.models.course_committee import CourseCommittee
from app.schemas.course_committee import (
    CourseCommitteeCreate,
    CourseCommitteeUpdate,
)
from datetime import datetime


def create_course_committee(db: Session, committee_data: CourseCommitteeCreate):
    new_committee = CourseCommittee(
        courseComId=committee_data.courseComId,
        prefix=committee_data.prefix,
        firstName=committee_data.firstName,
        lastName=committee_data.lastName,
        username=committee_data.username,
        password=committee_data.password,
        email=committee_data.email,
        phoneNumber=committee_data.phoneNumber,
        lastSeen=datetime.now().strftime("%d-%m-%Y %H.%M")
    )
    db.add(new_committee)
    db.commit()
    db.refresh(new_committee)
    return new_committee


def get_all_course_committees(db: Session):
    return db.query(CourseCommittee).all()


def get_course_committee(db: Session, committee_id: str):
    return db.query(CourseCommittee).filter(CourseCommittee.courseComId == committee_id).first()


def update_course_committee(db: Session, committee_id: str, committee_data: CourseCommitteeUpdate):
    committee_record = db.query(CourseCommittee).filter(CourseCommittee.courseComId == committee_id).first()
    if not committee_record:
        return None
    
    for key, value in committee_data.model_dump(exclude_unset=True).items():
        setattr(committee_record, key, value)

    db.commit()
    db.refresh(committee_record)
    return committee_record


def delete_course_committee(db: Session, committee_id: str):
    committee_record = db.query(CourseCommittee).filter(CourseCommittee.courseComId == committee_id).first()
    if committee_record:
        db.delete(committee_record)
        db.commit()
    return committee_record
