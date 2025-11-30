@echo off
echo Starting Rahagir AI Agent Server...
echo Access the interface at http://localhost:8000
python -m uvicorn api_server:app --reload
pause
