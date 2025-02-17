import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

origins = [
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # ระบุเฉพาะ Method ที่ต้องใช้
    allow_headers=["Authorization", "Content-Type"],  # ระบุเฉพาะ Headers ที่ต้องใช้
)

@app.get("/api/data")
def get_data():
    return {"data": "This is data from the backend"}