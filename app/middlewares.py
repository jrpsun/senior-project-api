from fastapi.middleware.cors import CORSMiddleware


def add_middleware(app):
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # ระบุเฉพาะ Method ที่ต้องใช้
    allow_headers=["Authorization", "Content-Type"],  # ระบุเฉพาะ Headers ที่ต้องใช้
)