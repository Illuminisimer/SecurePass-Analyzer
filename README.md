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
- Password strength scoring system (0–5+)  
- Detects weak password patterns  
- Checks personal information inside password:
  - Name  
  - Username  
  - Email prefix  
  - Date of birth  
- Common password blacklist detection  
- Detailed security report output  
- Reset and retry functionality  

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


# 📦 REQUIREMENTS

No external libraries required.

Built-in Python module used:

- tkinter  

---

# ⚙️ INSTALLATION & USAGE

Clone repository:
git clone https://github.com/your-username/SecurePasswordAnalyzer.git

Go to project folder:
cd SecurePasswordAnalyzer

Run project:
python main.py

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