# CLEANZO

A brief, one-sentence description of what Cleanzo does (e.g., "A Python-based data cleaning utility").

## Prerequisites

Before running this project, ensure you have Python installed.

## Getting Started

Follow these steps to set up the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com
cd cleanzo
```

### 2. Set Up Virtual Environment
Activate the environment (which you already have set up):
```powershell
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Running the Project
```bash
python main.py
```

## Project Structure
```text
CLEANZO/
│
├── venv/             # Virtual environment (ignored by git)
├── __init__.py       # Initializes the Cleanzo Python package
├── README.md         # Project documentation
└── main.py           # Main application entry point
```

## Deployment & Environment Variables

Set the following environment variables in your deployment (Render, Heroku, etc.) or locally before running the app:

- `SECRET_KEY`: A strong secret used to sign session cookies. Do NOT hardcode this in source.
- `ADMIN_PASSWORD`: (optional) Password used to create the initial `admin` account if it does not exist. Prefer setting a secure value in the host environment.
- `SUPERADMIN_PASSWORD`: (optional) Password used by `create_superadmin.py` to set/reset the superadmin password. If not set, the script will generate a secure random password and print it.

Example (PowerShell) locally:
```powershell
$env:SECRET_KEY = 'a-very-strong-secret'
$env:ADMIN_PASSWORD = 'choose-a-secure-password'
$env:SUPERADMIN_PASSWORD = 'another-secure-password'
python create_superadmin.py
```

Notes:
- The application no longer uses hardcoded admin passwords; it validates the submitted password against the stored hashed password for existing admin accounts.
- To rotate admin/superadmin passwords in production, update the corresponding env var and re-run `create_superadmin.py` (or manually update the user's password in the DB).
- Clearing or rotating `SECRET_KEY` will invalidate existing signed session cookies and force all users to re-login.
