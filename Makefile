VENV_DIR = venv


.PHONY: run
run:
	$(VENV_DIR)\Scripts\activate.bat
    uvicorn main:app --host 127.0.0.1 --port 8000 --reload
