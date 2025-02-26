from sqlalchemy import Column, String, ForeignKey, Integer
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantTraining(Base):
    __tablename__ = 'Applicant_Training'

    trainingId = Column(String(50), primary_key=True)
    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'))
    nameOfCourse = Column(String(255))
    institution = Column(String(255))
    year = Column(Integer)
    mode = Column(String(50))
    country = Column(String(50))
    trainingCer = Column(LONGTEXT)