from sqlalchemy import Column, String, Date, ForeignKey
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.admission import Admission


class ApplicantGeneralInformation(Base):
    __tablename__ = 'Applicant_General_Information'

    applicantId = Column(String(50), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'))
    idCardNumber = Column(String(50))
    idCardExpDate = Column(Date)
    password = Column(String(50))
    passportId = Column(String(50))
    passportExpDate = Column(String(50))
    gender = Column(String(50))
    prefix = Column(String(50))
    firstnameTH = Column(String(50), index=True)
    firstnameEN = Column(String(50), index=True)
    lastnameTH = Column(String(50), index=True)
    lastnameEN = Column(String(50), index=True)
    middlenameTH = Column(String(50), index=True)
    middlenameEN = Column(String(50), index=True)
    nicknameTH = Column(String(50), index=True)
    nicknameEN = Column(String(50), index=True)
    nationality = Column(String(50))
    birthDate = Column(String(50))
    livingCountry = Column(String(50))
    applicantPicture = Column(LONGTEXT)
    docCopyIdCard = Column(LONGTEXT)
    docCopyPassport = Column(LONGTEXT)
    docCopyHouseRegis = Column(LONGTEXT)