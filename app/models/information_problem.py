from sqlalchemy import Column, String, Text, ForeignKey
from app.db import Base
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations
from app.models.education_department import EducationDepartment


class InformationProblem(Base):
    __tablename__ = 'Information_Problem'

    problemId = Column(String(50), primary_key=True)
    educationId = Column(String(50), ForeignKey('Education_Department.educationId'))
    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'))
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'))
    details = Column(Text, nullable=True)
    updateDate = Column(String(50), nullable=True)