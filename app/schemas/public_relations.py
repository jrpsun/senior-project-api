from pydantic import BaseModel
from typing import Optional


class PublicRelationsBase(BaseModel):
    PRid: str
    firstName: str
    lastName: str
    username: str
    email: str
    phoneNumber: str


class PublicRelationsCreate(PublicRelationsBase):
    password: str


class PublicRelationsUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None
    password: Optional[str] = None


class PublicRelationsResponse(PublicRelationsBase):
    
    class Config:
        from_attributes = True  # ใช้กับ SQLAlchemy ORM Models เพื่อให้ Pydantic แปลง SQLAlchemy Model เป็น JSON ได้นะครับ
