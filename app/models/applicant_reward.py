from sqlalchemy import Column, String, Date, ForeignKey, Integer
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantReward(Base):
    __tablename__ = 'Applicant_Reward'

    rewardId = Column(String(50), primary_key=True)
    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'))
    nameOfCompetition = Column(String(255))
    year = Column(Integer)
    level = Column(String(50))
    awards = Column(String(255))
    project = Column(String(255))
    rewardCer = Column(LONGTEXT)