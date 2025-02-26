from sqlalchemy import Column, String, Text, ForeignKey, Integer
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantTalent(Base):
    __tablename__ = 'Applicant_Talent'

    rewardId = Column(String(50), primary_key=True)
    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'))
    kindOfTalent = Column(String(255))
    nameOfCompetition = Column(String(255))
    year = Column(Integer)
    awards = Column(String(255))
    url = Column(String(255))
    moreDetails = Column(Text)
    talentCer = Column(LONGTEXT)