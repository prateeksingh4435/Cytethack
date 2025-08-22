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
