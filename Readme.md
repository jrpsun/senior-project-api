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