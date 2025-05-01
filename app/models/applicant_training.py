from sqlalchemy import Column, String, ForeignKey
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations


class ApplicantTraining(Base):
    __tablename__ = 'Applicant_Training'

    trainingId = Column(String(50), primary_key=True)
    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    nameOfCourse = Column(String(255), nullable=True)
    institution = Column(String(255), nullable=True)
    trainingYear = Column(String(50), nullable=True)
    trainingMode = Column(String(50), nullable=True)
    trainingCountry = Column(String(50), nullable=True)
    trainingCer = Column(LONGTEXT, nullable=True)
    trainingCerName = Column(String(255), nullable=True)
    trainingCerSize = Column(String(50), nullable=True)