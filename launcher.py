import tkinter as tk
from tkinter import messagebox
import subprocess
import secrets

login_password = "admin123"

def open_admin():
    password = password_entry.get()
    if password == login_password:
        root.destroy()
        token = secrets.token_hex(16)
        subprocess.run(["python", "college_manager.py", token])
    else:
        messagebox.showerror("Error", "Incorrect password")

def open_user():
    root.destroy()
    token = secrets.token_hex(16)
    subprocess.run(["python", "college_recommender.py", token])

def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        show_password_button.config(text="Hide Password")
    else:
        password_entry.config(show='*')
        show_password_button.config(text="Show Password")

def show_password_entry():
    password_label.pack(pady=5)
    password_entry.pack()
    show_password_button.pack()
    submit_password.pack(pady=5)
    password_entry.focus()  # Focus cursor on password entry

# Main window setup
root = tk.Tk()
root.title("Career Council Login")
root.geometry("350x250")
root.config(bg="#f0f0f5")

# Bind "Enter" key to appropriate functions
root.bind('<Return>', lambda event: submit_password.invoke() if password_entry.winfo_ismapped() else open_user())

# Title Label
title_label = tk.Label(root, text="Welcome to Career Council", font=("Arial", 14, "bold"), bg="#f0f0f5", fg="#333333")
title_label.pack(pady=15)

# Admin/User buttons
login_type_label = tk.Label(root, text="Select your login type:", font=("Arial", 12), bg="#f0f0f5", fg="#333333")
login_type_label.pack(pady=10)

admin_button = tk.Button(root, text="Admin", width=12, font=("Arial", 10), bg="#4CAF50", fg="white", command=show_password_entry)
admin_button.pack(pady=5)

user_button = tk.Button(root, text="User", width=12, font=("Arial", 10), bg="#2196F3", fg="white", command=open_user)
user_button.pack(pady=5)

# Admin password entry and toggle
password_label = tk.Label(root, text="Enter Admin password:", font=("Arial", 10), bg="#f0f0f5", fg="#333333")
password_entry = tk.Entry(root, show="*", font=("Arial", 10))
show_password_button = tk.Button(root, text="Show Password", font=("Arial", 8), command=toggle_password)
submit_password = tk.Button(root, text="Submit", font=("Arial", 10), bg="#4CAF50", fg="white", command=open_admin)

root.mainloop()
