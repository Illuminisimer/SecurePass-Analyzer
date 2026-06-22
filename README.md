# 🔐 SECURE PASSWORD ANALYZER

A Python-based GUI application using Tkinter that analyzes password strength and security.

This tool checks:

- Password complexity rules  
- Personal information leakage (name, username, email, DOB)  
- Common password blacklist  
- Security scoring system  

---

# 🚀 FEATURES

- GUI-based interface using Tkinter  
- Password strength scoring system upgraded to a 0–100 ML-backed scale  
- Detects weak password patterns  
- Checks personal information inside password:
  - Name  
  - Username  
  - Email prefix  
  - Date of birth  
- Common password blacklist detection  
- Detailed security report output  
- Reset and retry functionality  
- Backend FastAPI analysis endpoint: `/api/analysis/score`  

---

# 🧠 HOW IT WORKS

## 🔹 Complexity Check
- Minimum length (8+ characters)  
- Uppercase letter check  
- Lowercase letter check  
- Digit check  
- Special character check  

---

## 🔹 Personal Information Check
The system checks if password contains:

- User's name  
- Username  
- Email prefix  
- Date of birth  

---

## 🔹 Common Password Check
Compares password with a known list of weak/common passwords.

---

# 📁 PROJECT STRUCTURE

SecurePasswordAnalyzer/

- main.py  
- common_passwords.txt  
- requirements.txt  
- README.md
- screenshot.png  

---

# 📦 REQUIREMENTS

This project now includes a FastAPI backend and a Next.js frontend.

Backend requirements:
- Python 3.11+ (recommended)
- `pip` for Python package installation

Frontend requirements:
- Node.js 20+
- npm or yarn

---

# ⚙️ INSTALLATION & USAGE

## Backend

1. Open PowerShell in the repository root:
   `cd d:\SecurePass-Analyzer`
2. Activate the Python virtual environment:
   `.\.venv\Scripts\Activate`
3. Install backend dependencies:
   `pip install -r backend/requirements.txt`
4. Start the FastAPI server:
   `uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000`
5. Confirm the backend is running at:
   `http://127.0.0.1:8000`

## Frontend

1. Open PowerShell in the frontend folder:
   `cd d:\SecurePass-Analyzer\frontend`
2. Install frontend dependencies:
   `npm install`
3. Start the Next.js development server:
   `npm run dev`
4. Open the app in your browser at:
   `http://127.0.0.1:3000`

## Desktop wrapper (optional)

A desktop Electron wrapper exists under `electron/` if you want a packaged app.

## UX Instructions

1. Open the frontend at `http://127.0.0.1:3000`.
2. Go to **Login** and register a new account with email and a strong master password.
3. After login, open the **Vault** dashboard.
4. Create a vault, then add entries using a title, username, URL, password, and optional notes.
5. To read a stored password, click **Decrypt** and enter your master password.
6. Enable multi-factor authentication at `/2fa` to generate a TOTP QR code and backup codes.
7. Visit `/assistant` for AI-driven password and security recommendations.

---

# �️ TROUBLESHOOTING

- If `uvicorn` is not found, ensure the virtual environment is activated and run `pip install -r backend/requirements.txt`.
- If `next` is not recognized, run `npm install` from `d:\SecurePass-Analyzer\frontend` and try `npm run dev` again.
- If the frontend cannot reach the backend, confirm `NEXT_PUBLIC_API_BASE` is set to `http://127.0.0.1:8000/api` and both servers are running.
- If login fails with a 401 error after registration, clear browser local storage and re-login.
- If 2FA setup returns an invalid code error, verify the TOTP app is synced and use the current code.
- If `npm install` reports vulnerabilities, run `npm audit fix` for safe fixes and `npm audit` to review remaining warnings before upgrading packages.

---

# 🔐 RECOMMENDED SECURITY

- Keep backend dependencies current and rerun `pip install -r backend/requirements.txt` after updates.
- Use a virtual environment for Python to isolate backend packages.
- Keep frontend packages up to date and verify `next`, `react`, and `eslint` versions when upgrading.
- Prefer `npm audit fix` for non-breaking updates and only use `npm audit fix --force` after review.

---

# 📊 COMMON PASSWORD DATA SOURCE

This project uses a publicly available password dataset:

SecLists Project:
https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt

This dataset is widely used in cybersecurity research and penetration testing.

---

# 🛡️ PASSWORD SCORING SYSTEM

Length ≥ 8 → +1  
Uppercase → +1  
Lowercase → +1  
Digit → +1  
Special character → +1  
Personal info found → -2  
Common password found → -2  

---

# 📌 STRENGTH LEVELS

0–2 → WEAK  
3–4 → MEDIUM  
5+ → STRONG  

---

# 🚀 FUTURE IMPROVEMENTS

- Progress bar strength meter  
- Real-time password checking  
- Dark mode UI  
- Export report as PDF  
- Password history tracking  

---

# 👨‍💻 AUTHOR

MD Sami Akhlaq

- 🔗 LinkedIn: https://www.linkedin.com/in/md-sami-akhlaq-2838b0334/  
- 🔗 Facebook: https://www.facebook.com/say.yashh 

# This project was built for learning purposes to understand:

- Python GUI development (Tkinter)  
- Password security concepts  
- Basic cybersecurity principles  

---

# 📜 LICENSE

MIT License recommended for open-source use.