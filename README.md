# Product & Analytics Management System

A full-stack enterprise analytics platform powered by **FastAPI** (Backend) and **Streamlit** (Frontend) with MySQL database support.

---

## ⚡ Quick Start (Single Command)

You can run both the Backend (FastAPI) and Frontend (Streamlit) together with a single command from the project root:

### Using Python:
```bash
python run.py
```

### Using PowerShell (Windows):
```powershell
.\run.ps1
```

### Using Command Prompt / Double Click (Windows):
```cmd
run.bat
```

### Using Bash (Linux / macOS):
```bash
chmod +x run.sh
./run.sh
```

---

## 🌐 Service URLs

Once running, access the services at:
- **Frontend Dashboard (Streamlit):** [http://localhost:8501](http://localhost:8501)
- **Backend API (FastAPI):** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## ⚙️ Optional Launch Arguments

`run.py` accepts several custom parameters:

```bash
# Custom ports
python run.py --backend-port 8000 --frontend-port 8501

# Run Streamlit in headless mode (doesn't auto-open browser tab)
python run.py --headless

# Disable backend auto-reload
python run.py --no-reload

# View all options
python run.py --help
```

---

## 🛑 Stopping Services

Press `Ctrl + C` in the terminal at any time. The runner will gracefully terminate both the FastAPI server and the Streamlit application cleanly without leaving orphaned background processes.
