from sqlalchemy import Column, String, ForeignKey
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations


class ApplicantReward(Base):
    __tablename__ = 'Applicant_Reward'

    rewardId = Column(String(50), primary_key=True)
    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    nameOfCompetition = Column(String(255), nullable=True)
    rewardYear = Column(String(50), nullable=True)
    rewardLevel = Column(String(50), nullable=True)
    rewardAwards = Column(String(255), nullable=True)
    project = Column(String(255), nullable=True)
    rewardCer = Column(LONGTEXT, nullable=True)
    rewardCerName = Column(String(255), nullable=True)
    rewardCerSize = Column(String(50), nullable=True)