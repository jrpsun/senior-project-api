from sqlalchemy import Column, String, Text, ForeignKey, Integer
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantTalent(Base):
    __tablename__ = 'Applicant_Talent'

    talentId = Column(String(50), primary_key=True)
    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'))
    kindOfTalent = Column(String(255), nullable=True)
    nameOfCompetition = Column(String(255), nullable=True)
    talentYear = Column(Integer, nullable=True)
    talentAwards = Column(String(255), nullable=True)
    url = Column(String(255), nullable=True)
    moreDetails = Column(Text, nullable=True)
    talentCer = Column(LONGTEXT, nullable=True)