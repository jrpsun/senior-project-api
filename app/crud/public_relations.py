from sqlalchemy.orm import Session
from app.models.public_relations import PublicRelations
from app.schemas.public_relations import PublicRelationsCreate, PublicRelationsUpdate
from datetime import datetime

# 🔹 Create (เพิ่ม Public Relations)
def create_public_relation(db: Session, pr_data: PublicRelationsCreate):
    new_pr = PublicRelations(
        PRid=pr_data.PRid,
        prefix=pr_data.prefix,
        firstName=pr_data.firstName,
        lastName=pr_data.lastName,
        username=pr_data.username,
        password=pr_data.password,
        email=pr_data.email,
        phoneNumber=pr_data.phoneNumber,
        lastSeen=datetime.now().strftime("%d-%m-%Y %H.%M")
    )
    db.add(new_pr)
    db.commit()
    db.refresh(new_pr)
    return new_pr

# 🔹 Read (ดึงข้อมูลทั้งหมด)
def get_public_relations(db: Session):
    return db.query(PublicRelations).all()

# 🔹 Read (ดึงข้อมูลตาม ID)
def get_public_relation_by_id(db: Session, pr_id: str):
    return db.query(PublicRelations).filter(PublicRelations.PRid == pr_id).first()

# 🔹 Update (แก้ไขข้อมูล)
def update_public_relation(db: Session, pr_id: str, pr_data: PublicRelationsUpdate):
    pr_record = db.query(PublicRelations).filter(PublicRelations.PRid == pr_id).first()
    if not pr_record:
        return None

    for key, value in pr_data.model_dump(exclude_unset=True).items():
        setattr(pr_record, key, value)

    db.commit()
    db.refresh(pr_record)
    return pr_record

# 🔹 Delete (ลบ Public Relations)
def delete_public_relation(db: Session, pr_id: str):
    pr_record = db.query(PublicRelations).filter(PublicRelations.PRid == pr_id).first()
    if pr_record:
        db.delete(pr_record)
        db.commit()
    return pr_record
