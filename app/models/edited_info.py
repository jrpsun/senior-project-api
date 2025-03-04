from sqlalchemy import Column, String, Text, ForeignKey
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.applicant_general_information import ApplicantGeneralInformation
from app.models.public_relations import PublicRelations


class EditedInfo(Base):
    __tablename__ = 'Edited_Info'

    editId = Column(String(50), primary_key=True)
    PRid = Column(String(50), ForeignKey('Public_Relations.PRid'))
    applicantId = Column(String(50), ForeignKey('Applicant_General_Information.applicantId'))
    editDate = Column(String(50), nullable=True)
    details = Column(Text, nullable=True)