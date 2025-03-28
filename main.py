import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.middlewares import add_middleware
from app.db import engine, Base, get_db
from app.models import *
from app.routers import (
    public_relations,
    interview_committee,
    education_department,
    course_committee,
    admisstion,
    applicant,
    excel,
    upload,
)

load_dotenv()
app = FastAPI()
add_middleware(app)
Base.metadata.create_all(bind=engine)


app.include_router(public_relations.router, prefix="/public-relations", tags=["Public Relations"])
app.include_router(interview_committee.router, prefix="/interview-committee", tags=["Interview Committee"])
app.include_router(education_department.router, prefix="/education-department", tags=["Education Department"])
app.include_router(course_committee.router, prefix="/course-committee", tags=["Course Committee"])
app.include_router(admisstion.router, prefix="/admission", tags=["Admission"])
app.include_router(applicant.router, prefix="/applicant", tags=["Applicant"])
app.include_router(excel.router, prefix="/excel", tags=["Excel"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])


@app.get("/api/data")
def get_data():
    return {"data": "This is data from the backend"}