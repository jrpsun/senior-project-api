from sqlalchemy import Column, String, Text, ForeignKey, Integer
from app.db import Base
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.course_committee import CourseCommittee


class PreliminaryEvaluation(Base):
    __tablename__ = 'Preliminary_Evaluation'

    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'), primary_key=True)
    courseComId = Column(String(50), ForeignKey('Course_Committee.courseComId'))
    preliminaryEva = Column(String(255), nullable=True)
    preliminaryComment = Column(Text, nullable=True)
    preEvaDate = Column(String(255), nullable=True)