from sqlalchemy.orm import Session
from app.models.interview_committee import InterviewCommittee
from app.schemas.interview_committee import (
    InterviewCommitteeCreate,
    InterviewCommitteeUpdate
)
from datetime import datetime


def create_interview_committee(db: Session, ic_data: InterviewCommitteeCreate):
    new_ic = InterviewCommittee(
        interviewComId=ic_data.interviewComId,
        prefix=ic_data.prefix,
        firstName=ic_data.firstName,
        lastName=ic_data.lastName,
        username=ic_data.username,
        password=ic_data.password,
        email=ic_data.email,
        phoneNumber=ic_data.phoneNumber,
        lastSeen=datetime.now().strftime("%d-%m-%Y %H.%M")
    )
    db.add(new_ic)
    db.commit()
    db.refresh(new_ic)
    return new_ic


def get_interview_committees(db: Session):
    return db.query(InterviewCommittee).all()


def get_interview_committee_by_id(db: Session, ic_id: str):
    return db.query(InterviewCommittee).filter(InterviewCommittee.interviewComId == ic_id).first()


def update_interview_committee(db: Session, ic_id: str, ic_data: InterviewCommitteeUpdate):
    ic_record = db.query(InterviewCommittee).filter(InterviewCommittee.interviewComId == ic_id).first()
    if not ic_record:
        return None

    for key, value in ic_data.model_dump(exclude_unset=True).items():
        setattr(ic_record, key, value)

    db.commit()
    db.refresh(ic_record)
    return ic_record


def delete_interview_committee(db: Session, ic_id: str):
    ic_record = db.query(InterviewCommittee).filter(InterviewCommittee.interviewComId == ic_id).first()
    if ic_record:
        db.delete(ic_record)
        db.commit()
    return ic_record