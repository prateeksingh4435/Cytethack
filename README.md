git clone https://github.com/prateeksingh4435/Cytethack.git

cd Process

# Create virtual environment
python -m venv venv

venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver



# To build EXE

pip install pyinstaller

pyinstaller --onefile agent.py


The EXE will be available in dist/agent.exe
Double-click agent.exe → It will collect process data and send it to backend.

Open http://127.0.0.1:8000/monitor  in a browser
The page fetches the latest process data from backend and displays it in a collapsible tree view.

Click Refresh to load updated process details.


# API Specification 

1. Send Process Data
2. 
   POST /api/process/
   
   Headers:

  API-Key: <your-api-key>
  Payload Example:
  
    {
    "hostname": "DESKTOP-1234",
    "timestamp": "2025-08-22T12:00:00",
    "processes": [
    {  
      "pid": 1234,
      "name": "chrome.exe",
      "cpu": 12.5,
      "memory": 100.4,
      "parent_pid": 1
      }
    ]
    }

  Response Example:
  {"status": "success", "message": "Data stored successfully"}

# Get Latest Process Data

GET /api/process/<hostname>/latest/

Response Example:

{
  "hostname": "DESKTOP-1234",
  "timestamp": "2025-08-22T12:00:00",
  "processes": [
    {
      "pid": 1234,
      "name": "chrome.exe",
      "cpu": 12.5,
      "memory": 100.4,
      "children": [
        {
          "pid": 5678,
          "name": "chrome_subprocess.exe",
          "cpu": 3.4,
          "memory": 45.6
        }
      ]
    }
  ]
}

# Flow 
Windows Agent → Django API → SQLite DB → Frontend (index.html)

