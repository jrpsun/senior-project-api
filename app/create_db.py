import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import engine, Base
from models import *


def create_database():
    Base.metadata.create_all(bind=engine)
    print("Database created successfully!")

if __name__ == "__main__":
    create_database()
