# Seneior-Project-Backend

## How to run project (window edition)
สร้าง envarinment ด้วย คำสั่ง
```bash
python -m venv venv
```
ติดตั้ง libray ต่างๆในไฟล์ requirements.txt ด้วยคำสั่ง
```bash
pip install -r requirements.txt
```
start server
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## How to migrate database (alembic)
หลังจากแก้ไข models แล้ว สร้างคำสั่ง migration ด้วยคำสั่ง
```bash
alembic revision --autogenerate -m "message"
```

รัน migration ที่ทำการแก้ไขแล้วด้วยคำสั่ง
```bash
alembic upgrade head
```
