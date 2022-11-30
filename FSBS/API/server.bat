@echo off
cd ..\..
Runtimes\Python\venv\Scripts\python.exe -m uvicorn FSBS.API.api:api --reload --ssl-keyfile "FSBS/API/ssl/key.pem" --ssl-certfile "FSBS/API/ssl/cert.pem" --port 8000 --host "127.0.0.1"