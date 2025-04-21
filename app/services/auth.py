from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Request, Response, status
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.applicant_general_information import ApplicantGeneralInformation

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET = os.getenv("REFRESH_SECRET")
ALGORITHM = os.getenv("ALGORITHM")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, expires_delta: timedelta, secret=SECRET_KEY):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)


def decode_token(token: str, secret=SECRET_KEY):
    return jwt.decode(token, secret, algorithms=[ALGORITHM])


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        app_id: str = payload.get("appId")
        if app_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(ApplicantGeneralInformation).filter_by(applicantId=app_id).first()
    if user is None:
        raise credentials_exception

    return user


def perform_refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=[ALGORITHM])
        app_id = payload.get("appId")
        if not app_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = db.query(ApplicantGeneralInformation).filter_by(applicantId=app_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        new_access_token = create_token(
            data={"sub": user.firstnameEN +" "+ user.lastnameEN, "appId": user.applicantId},
            expires_delta=timedelta(minutes=60)
        )

        return {"access_token": new_access_token}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")