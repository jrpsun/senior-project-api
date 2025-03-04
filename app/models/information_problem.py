from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.education_department import EducationDepartment


class InformationProblem(Base):
    __tablename__ = 'Information_Problem'

    problemId = Column(String(50), primary_key=True)
    educationId = Column(String(50), ForeignKey('Education_Department.educationId'))
    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'))
    details = Column(Text, nullable=True)
    updateDate = Column(String(50), nullable=True)