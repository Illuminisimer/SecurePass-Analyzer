
# 🔐 SECURE PASSWORD ANALYZER

Secure Password Analyzer is a powerful open-source security tooling project that helps individuals and teams evaluate password strength, detect weak or exposed credentials, and securely manage encrypted password vaults. It combines a FastAPI backend, a Next.js frontend, and an optional Electron desktop wrapper to provide a complete, audit-ready workflow for password analysis, storage, and retrieval.

The project is designed for security-conscious developers, system administrators, and privacy-aware users who want a local, extensible solution to analyze password hygiene and safely store secrets.

---

# 🚀 FEATURES

- **Comprehensive password analysis**: Multi-factor checks including length, complexity, pattern detection, and blacklist comparisons.
- **Personal information detection**: Flags passwords that contain user attributes such as name, username, email prefix, or date-of-birth patterns.
- **Common-password blacklist**: Uses a curated list of frequently-used and easily-guessable passwords to detect risky choices.
- **Scoring system**: Produces clear strength scores and labels to help users understand risk and remediation steps.
- **Vault management**: Create encrypted vaults, add entries, and decrypt with a master password.
- **Authentication + 2FA**: Built-in account registration, login, and optional TOTP-based multi-factor authentication.
- **Programmatic API**: FastAPI backend exposes analysis endpoints for integration and automation (`/api/analysis/score`).
- **AI assistant**: An optional assistant endpoint that can provide contextual recommendations and password hardening tips.
- **Cross-platform desktop option**: Electron wrapper for users who prefer a packaged local application.
- **Extensible architecture**: Clear separation of frontend, backend, and services to simplify feature additions and security reviews.

This feature set makes the project useful for real-world password auditing, user training, and as a foundation for larger secrets-management systems.

---

# 🧠 HOW IT WORKS

The Secure Password Analyzer assesses and manages passwords through a modular pipeline:

- **Client input**: The Next.js frontend (or Electron UI) collects passwords and optional account metadata.
- **API request**: The frontend calls the FastAPI backend endpoints (for analysis, vault actions, auth, and assistant queries).
- **Validation & auth**: Authentication, registration, and TOTP flows are handled by the backend services and JWT utilities.
- **Analysis pipeline**:
  - Complexity checks: minimum length, uppercase, lowercase, digits, and special characters.
  - Pattern detection: repeated characters, sequential patterns, and common weak patterns.
  - Personal-information scan: checks for name, username, email prefix, and date-of-birth fragments.
  - Blacklist comparison: against `common_passwords.txt` and other curated lists.
  - Scoring aggregation: a composite score is computed and normalized to human-friendly labels (WEAK / MEDIUM / STRONG).
- **Reporting**: Backend returns a structured analysis result and suggested remediation steps.
- **Vault operations**: Encrypted entries are stored in the backend database; decryption requires the user's master password and enforces access controls.
- **Optional AI guidance**: The assistant service can analyze results and return tailored recommendations.

---

## 🔹 Personal Information Check

This check inspects whether a candidate password contains fragments or exact matches of personal attributes that significantly weaken security:

- **Fields inspected**: user full name, username, email local part (before @), and common date formats (YYYY, YY, MMDD, DDMM, YYYYMMDD).
- **Matching strategy**: exact substring matches, common leetspeak substitutions (e.g., 0→o, 1→l), and normalized whitespace/punctuation removal to surface disguised matches.
- **Impact on score**: detected personal information reduces the overall strength score and is flagged prominently in the analysis report with mitigation advice (avoid names, dates, and reuse of identifiable tokens).

This helps prevent easy targeted-guess attacks and social-engineering vulnerabilities.

---

# 📁 PROJECT STRUCTURE

Top-level layout (abridged):

- `backend/` — FastAPI backend and services
  - `app/main.py` — FastAPI application entry
  - `app/api/` — API route modules (analysis, assistant, auth, otp, vault)
  - `app/services/` — Business logic and helpers (analysis pipeline, encryption, jwt, otp, password utilities)
  - `app/models/` — ORM/data models (users, vault entries, audit logs)
  - `app/schemas/` — Pydantic request/response schemas
  - `database/` — DB connection utilities

- `frontend/` — Next.js React application
  - `app/` — pages and routing (login, 2fa, assistant, vault pages)
  - `components/` — UI components (Button, Card, FormField, Modal)
  - `lib/` — client helpers (API client, utils)

- `electron/` — Optional Electron wrapper for desktop packaging

- project root files: `main.py`, `common_passwords.txt`, `README.md`, and repository-level scripts

This separation makes it straightforward to review security-sensitive code (backend services and encryption) independently from UI concerns.

---

# 📦 REQUIREMENTS

Minimum supported platforms and tooling:

- Backend
  - Python 3.11+
  - Recommended: a virtual environment (`venv` or similar)
  - Install with: `pip install -r backend/requirements.txt`

- Frontend
  - Node.js 20+ and npm or yarn
  - Install with: `npm install` (run in `frontend/`)

- Desktop wrapper (optional)
  - Node.js + Electron build toolchain (see `electron/package.json`)

- Runtime ports
  - Backend default: `127.0.0.1:8000` (FastAPI /uvicorn)
  - Frontend default: `127.0.0.1:3000` (Next.js dev server)


# 🚀 Installation (How to use it)

## 1. Backend (from repository root):

1. Open PowerShell or CMD in the repository root:
   `cd d:\SecurePass-Analyzer`
2. Activate the Python virtual environment:
   `.\.venv\Scripts\Activate`
3. Install backend dependencies:
   `pip install -r backend/requirements.txt`
4. Start the FastAPI server:
   `uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000`
5. Confirm the backend is running at:
   `http://127.0.0.1:8000`

## 2. Frontend (in a separate terminal):

1. Open PowerShell or CMD in the frontend folder:
   `cd d:\SecurePass-Analyzer\frontend`
2. Install frontend dependencies:
   `npm install`
3. Start the Next.js development server:
   `npm run dev`
4. Open the app in your browser at:
   `http://127.0.0.1:3000`

## 3. Desktop Electron Wrapper (optional):

```powershell
cd d:\SecurePass-Analyzer\electron
npm install
# follow package.json scripts to build/package
```

---

# 💻 UX Instructions

1. Open the frontend at `http://127.0.0.1:3000`.
2. Go to **Login** and register a new account with email and a strong master password.
3. After login, open the **Vault** dashboard.
4. Create a vault, then add entries using a title, username, URL, password, and optional notes.
5. To read a stored password, click **Decrypt** and enter your master password.
6. Enable multi-factor authentication at `/2fa` to generate a TOTP QR code and backup codes.
7. Visit `/assistant` for AI-driven password and security recommendations.

---



## ⚙️ TROUBLESHOOTING & SECURITY NOTES

- If `uvicorn` is not found, confirm your virtual environment is active and dependencies are installed.
- If the frontend cannot reach the backend, verify `NEXT_PUBLIC_API_BASE` is set to `http://127.0.0.1:8000/api` in the frontend environment.
- For reproducible deployments, pin backend dependencies and run security audits (`pip-audit`, `npm audit`).
- Keep secret material out of version control. Use environment variables for keys and secrets.
- The password blacklist is derived from public SecLists data; review and update `common_passwords.txt` periodically.

---

## 🔐 RECOMMENDED SECURITY

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

# 👨‍💻 AUTHOR

# 1. MD Sami Akhlaq (Creator)
- Created the main Security engine.
- 🔗 LinkedIn: https://www.linkedin.com/in/md-sami-akhlaq-2838b0334/  
- 🔗 Facebook: https://www.facebook.com/say.yashh 

# 2. Ahnaf Wasi Azad (Full stack developer)
- Created the entire frontend, backend and the desktop wrapper
- implemented database
- security checks
- improved the overall tool
- 🔗 Email : ahnafasi.awa@gmail.com
- 🔗 Github : https://github.com/Illuminisimer
- 🔗 Facebook : https://www.facebook.com/Illuminisimer
---

# 📜 LICENSE

MIT License recommended for open-source use.

---