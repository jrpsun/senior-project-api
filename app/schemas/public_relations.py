from pydantic import BaseModel
from typing import Optional


class PublicRelationsBase(BaseModel):
    PRid: str
    prefix: str
    firstName: str
    lastName: str
    username: str
    email: str
    phoneNumber: str


class PublicRelationsCreate(PublicRelationsBase):
    password: str


class PublicRelationsUpdate(BaseModel):
    prefix: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None


class PublicRelationsResponse(PublicRelationsBase):
    lastSeen: Optional[str] = None
    
    class Config:
        from_attributes = True  # ใช้กับ SQLAlchemy ORM Models เพื่อให้ Pydantic แปลง SQLAlchemy Model เป็น JSON ได้นะครับ
