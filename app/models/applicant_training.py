from sqlalchemy import Column, String, ForeignKey, Integer
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation


class ApplicantTraining(Base):
    __tablename__ = 'Applicant_Training'

    trainingId = Column(String(50), primary_key=True)
    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'))
    nameOfCourse = Column(String(255), nullable=True)
    institution = Column(String(255), nullable=True)
    trainingYear = Column(String(50), nullable=True)
    trainingMode = Column(String(50), nullable=True)
    trainingCountry = Column(String(50), nullable=True)
    trainingCer = Column(LONGTEXT, nullable=True)
    trainingCerName = Column(String(255), nullable=True)
    trainingCerSize = Column(String(50), nullable=True)