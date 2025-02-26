from sqlalchemy import Column, String, Date, ForeignKey, Float
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantCambridgeIGCSEEnglish(Base):
    __tablename__ = 'Applicant_Cambridge_IGCSE_English'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    igcseType = Column(String(50))
    score = Column(Float)
    testDate = Column(Date)
    cambridgeCer = Column(LONGTEXT)