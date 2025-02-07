import tkinter as tk
from tkinter import messagebox
import sqlite3

# Fungsi untuk membuat database pengguna
def create_user_db():
    conn = sqlite3.connect('user_db.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )""")
    conn.commit()
    conn.close()

# Fungsi untuk menambah akun baru
def create_account(username, password):
    conn = sqlite3.connect('user_db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Fungsi untuk login pengguna
def login(username, password):
    conn = sqlite3.connect('user_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Fungsi untuk logout
def logout(current_user):
    current_user = None
    return current_user

# Fungsi untuk menampilkan akun saya (hanya setelah login)
def show_account(current_user):
    if current_user:
        messagebox.showinfo("Akun Saya", f"Username: {current_user[0]}")
    else:
        messagebox.showerror("Error", "Anda belum login!")

# Fungsi untuk menampilkan form login
def show_login(root, update_menu_for_logged_in):
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x200")
    
    tk.Label(login_window, text="Username").pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=10)
    
    tk.Label(login_window, text="Password").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=10)
    
    def do_login():
        username = username_entry.get()
        password = password_entry.get()
        
        user = login(username, password)
        if user:
            update_menu_for_logged_in()
            login_window.destroy()
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")
    
    tk.Button(login_window, text="Login", command=do_login).pack(pady=20)

# Fungsi untuk mengupdate menu setelah login
def update_menu_for_logged_in(login_menu):
    login_menu.entryconfig("Login", state="disabled")
    login_menu.entryconfig("Logout", state="normal")
    login_menu.entryconfig("Akun Saya", state="normal")

# Fungsi untuk mengupdate menu setelah logout
def update_menu_for_logged_out(login_menu):
    login_menu.entryconfig("Login", state="normal")
    login_menu.entryconfig("Logout", state="disabled")
    login_menu.entryconfig("Akun Saya", state="disabled")
