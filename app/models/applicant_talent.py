from sqlalchemy import Column, String, Text, ForeignKey
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations


class ApplicantTalent(Base):
    __tablename__ = 'Applicant_Talent'

    talentId = Column(String(50), primary_key=True)
    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    kindOfTalent = Column(String(255), nullable=True)
    nameOfCompetition = Column(String(255), nullable=True)
    talentYear = Column(String(50), nullable=True)
    talentAwards = Column(String(255), nullable=True)
    url = Column(String(255), nullable=True)
    moreDetails = Column(Text, nullable=True)
    talentCer = Column(LONGTEXT, nullable=True)
    talentCerName = Column(String(255), nullable=True)
    talentCerSize = Column(String(50), nullable=True)