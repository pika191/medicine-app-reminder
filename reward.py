import random
import tkinter.messagebox as messagebox

def check_reward():
    reward = random.choice(['Badge: Hero of Health', 'Bonus Points: 100'])
    messagebox.showinfo("Reward", f"Selamat! Anda mendapatkan: {reward}")
