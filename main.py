import tkinter as tk

from backend.app.services.analysis import PasswordStrengthAnalyzer

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Secure Password Analyzer")
root.geometry("600x600")

# ---------------- INPUT FIELDS ----------------
tk.Label(root, text="Full Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Username").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="DOB (DDMMYYYY)").pack()
dob_entry = tk.Entry(root)
dob_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# ---------------- OUTPUT BOX ----------------
output = tk.Text(root, height=25, width=70)
output.pack()

# ---------------- CHECK PASSWORD ----------------
def check_password():
    password = password_entry.get()
    name = name_entry.get().strip()
    username = username_entry.get().strip()
    email = email_entry.get().strip()
    dob = dob_entry.get().strip()

    output.delete("1.0", tk.END)
    output.insert(tk.END, "🔐 PASSWORD SECURITY REPORT\n")
    output.insert(tk.END, "================================\n")

    analyzer = PasswordStrengthAnalyzer()
    result = analyzer.analyze_password(
        password,
        name=name,
        username=username,
        email=email,
        dob=dob,
    )

    output.insert(tk.END, f"Score: {result['score']} / 100\n")
    output.insert(tk.END, f"Grade: {result['grade']}\n")
    output.insert(tk.END, f"Entropy: {result['entropy']} bits\n")
    output.insert(tk.END, f"Confidence: {result['ml_confidence'] * 100:.0f}%\n")
    output.insert(tk.END, "================================\n")

    output.insert(tk.END, "Reasons:\n")
    for reason in result["reasons"]:
        output.insert(tk.END, f"- {reason}\n")

    output.insert(tk.END, "\nSuggestions:\n")
    for suggestion in result["suggestions"]:
        output.insert(tk.END, f"- {suggestion}\n")

    if result["common_password"]:
        output.insert(tk.END, "\n⚠ Warning: This password is found in common password lists.\n")

    if result["personal_info_matches"]:
        output.insert(tk.END, "\n⚠ Personal information detected in password: ")
        output.insert(tk.END, ", ".join(result["personal_info_matches"]) + "\n")

# ---------------- RESET FUNCTION ----------------
def reset():
    password_entry.delete(0, tk.END)
    output.delete("1.0", tk.END)
    password_entry.focus()

# ---------------- BUTTONS ----------------
tk.Button(root, text="Check Password", command=check_password).pack(pady=5)
tk.Button(root, text="Check Again", command=reset).pack(pady=5)
tk.Button(root, text="Quit", command=root.quit).pack(pady=5)

# ---------------- RUN ----------------
root.mainloop()