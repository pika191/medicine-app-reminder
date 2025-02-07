import tkinter as tk
from tkinter import messagebox
import time
from database import create_db, save_history, get_history
from notifikasi import send_notification
from edukasi import open_educational_video
from reward import check_reward
import schedule
import threading

# Fungsi untuk menjadwalkan pengingat
def schedule_notification():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Fungsi untuk menampilkan riwayat minum obat
def show_history():
    records = get_history()
    history_window = tk.Toplevel(root)
    history_window.title("Riwayat Minum Obat")
    history_window.geometry("600x300")
    history_text = tk.Text(history_window, width=70, height=15, font=("Arial", 12), wrap="word")
    history_text.pack(padx=20, pady=20)
    for record in records:
        history_text.insert(tk.END, f"Obat: {record[1]}, Dosis: {record[2]}, Tanggal: {record[0]}\n")

# Fungsi untuk mengatur pengingat minum obat
def schedule_medicine():
    medicine = medicine_entry.get()
    dose = dose_entry.get()

    if not medicine or not dose:
        messagebox.showerror("Error", "Nama obat dan dosis harus diisi!")
        return

    # Menyimpan riwayat minum obat
    save_history(medicine, dose)
    # Menambahkan notifikasi ke jadwal
    schedule.every().day.at(reminder_time_entry.get()).do(send_notification, medicine=medicine, dose=dose)
    check_reward()
    messagebox.showinfo("Pengingat Ditetapkan", f"Pengingat minum obat {medicine} pada jam {reminder_time_entry.get()} telah ditetapkan.")

# Fungsi untuk menampilkan dosis anjuran
def show_dose_anjuran(medicine):
    dosis_anjuran = {
        "Paracetamol": "500mg setiap 4-6 jam sekali.",
        "Ibuprofen": "200mg setiap 4-6 jam sekali.",
        "Aspirin": "325mg setiap 4-6 jam sekali.",
    }
    if medicine in dosis_anjuran:
        return dosis_anjuran[medicine]
    else:
        return "Dosis tidak diketahui. Harap cek label obat."

# Main UI
def main_window():
    global medicine_entry, dose_entry, reminder_time_entry, root
    root = tk.Tk()
    root.title("Pengingat Minum Obat")
    root.geometry("700x500")  # Ukuran jendela utama
    root.config(bg="#f0f0f0")

    # Frame untuk input data obat
    input_frame = tk.Frame(root, bg="#f0f0f0")
    input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    medicine_label = tk.Label(input_frame, text="Nama Obat:", font=("Arial", 12), bg="#f0f0f0")
    medicine_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    medicine_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
    medicine_entry.grid(row=0, column=1, padx=10, pady=5)

    dose_label = tk.Label(input_frame, text="Dosis (misal: 500mg):", font=("Arial", 12), bg="#f0f0f0")
    dose_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    dose_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
    dose_entry.grid(row=1, column=1, padx=10, pady=5)

    reminder_time_label = tk.Label(input_frame, text="Waktu Pengingat (format: HH:MM):", font=("Arial", 12), bg="#f0f0f0")
    reminder_time_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    reminder_time_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
    reminder_time_entry.grid(row=2, column=1, padx=10, pady=5)

    # Frame untuk tombol-tombol aksi
    action_frame = tk.Frame(root, bg="#f0f0f0")
    action_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    schedule_button = tk.Button(action_frame, text="Jadwalkan Minum Obat", command=schedule_medicine, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=20, height=2, relief="flat")
    schedule_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    history_button = tk.Button(action_frame, text="Riwayat Minum Obat", command=show_history, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", width=20, height=2, relief="flat")
    history_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    educasi_button = tk.Button(action_frame, text="Tonton Video Edukasi", command=open_educational_video, font=("Arial", 12, "bold"), bg="#FF9800", fg="white", width=20, height=2, relief="flat")
    educasi_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Mengatur ukuran grid agar responsif
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    input_frame.grid_rowconfigure(0, weight=1)
    input_frame.grid_rowconfigure(1, weight=1)
    input_frame.grid_rowconfigure(2, weight=1)
    input_frame.grid_columnconfigure(0, weight=1)
    input_frame.grid_columnconfigure(1, weight=2)

    action_frame.grid_rowconfigure(0, weight=1)
    action_frame.grid_rowconfigure(1, weight=1)
    action_frame.grid_columnconfigure(0, weight=1)
    action_frame.grid_columnconfigure(1, weight=1)

    root.mainloop()

# Menjalankan aplikasi
if __name__ == "__main__":
    create_db()
    # Menjalankan thread untuk pengingat otomatis
    threading.Thread(target=schedule_notification, daemon=True).start()
    main_window()
