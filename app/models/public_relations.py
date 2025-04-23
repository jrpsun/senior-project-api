from sqlalchemy import Column, String
from app.db import Base


class PublicRelations(Base):
    __tablename__ = 'Public_Relations'

    PRid = Column(String(50), primary_key=True)
    prefix = Column(String(50))
    firstName = Column(String(50))
    lastName = Column(String(50))
    username = Column(String(50))
    password = Column(String(255))
    email = Column(String(50))
    phoneNumber = Column(String(50))
    lastSeen = Column(String(50), nullable=True)