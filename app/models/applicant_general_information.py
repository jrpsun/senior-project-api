from sqlalchemy import Column, String, ForeignKey
from app.db import Base
from sqlalchemy.dialects.mysql import LONGTEXT
from app.models.admission import Admission
from app.models.applicant_registrations import ApplicantRegistrations


class ApplicantGeneralInformation(Base):
    __tablename__ = 'Applicant_General_Information'

    applicantId = Column(String(50), ForeignKey('ApplicantRegistrations.applicantId'), primary_key=True)
    programRegistered = Column(String(50), ForeignKey('Admission.admissionId'), primary_key=True)
    applicant_number = Column(String(50), nullable=True)
    #idCardNumber = Column(String(50), nullable=True)
    idCardExpDate = Column(String(50), nullable=True)
    #password = Column(String(255), nullable=True)
    #passportId = Column(String(50), nullable=True)
    passportExpDate = Column(String(50), nullable=True)
    gender = Column(String(50), nullable=True)
    #prefix = Column(String(50), nullable=True)
    #firstnameTH = Column(String(50), nullable=True, index=True)
    #firstnameEN = Column(String(50), nullable=True, index=True)
    #lastnameTH = Column(String(50), nullable=True, index=True)
    #lastnameEN = Column(String(50), nullable=True, index=True)
    middlenameTH = Column(String(50), nullable=True, index=True)
    middlenameEN = Column(String(50), nullable=True, index=True)
    nicknameTH = Column(String(50), nullable=True, index=True)
    nicknameEN = Column(String(50), nullable=True, index=True)
    #nationality = Column(String(50), nullable=True)
    birthDate = Column(String(50), nullable=True)
    livingCountry = Column(String(50), nullable=True)
    applicantPicture = Column(LONGTEXT, nullable=True)
    docCopyIdCard = Column(LONGTEXT, nullable=True)
    docCopyIdCardName = Column(String(255), nullable=True)
    docCopyIdCardSize = Column(String(50), nullable=True)
    docCopyPassport = Column(LONGTEXT, nullable=True)
    docCopyPassportName = Column(String(255), nullable=True)
    docCopyPassportSize = Column(String(50), nullable=True)
    docCopyHouseRegis = Column(LONGTEXT, nullable=True)
    docCopyHouseRegisName = Column(String(255), nullable=True)
    docCopyHouseRegisSize = Column(String(50), nullable=True)