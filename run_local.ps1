Write-Host "Starting MediFlow AI Native Setup (No Docker required)..."
Write-Host "Creating Python Virtual Environment..."
cd mediflow-backend
python -m venv venv

Write-Host "Installing Python Dependencies..."
.\venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Starting FastAPI Backend..."
Start-Process -NoNewWindow -FilePath ".\venv\Scripts\uvicorn.exe" -ArgumentList "main:app", "--host", "127.0.0.1", "--port", "8001"

cd ..\mediflow-frontend
Write-Host "Installing Node Dependencies..."
npm install

Write-Host "Starting React Frontend..."
npm run dev
