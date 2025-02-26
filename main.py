import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.middlewares import add_middleware
from app.db import engine, Base
from app.models import *

load_dotenv()
app = FastAPI()
add_middleware(app)
Base.metadata.create_all(bind=engine)


@app.get("/api/data")
def get_data():
    return {"data": "This is data from the backend"}