from plyer import notification

def send_notification(medicine, dose):
    notification.notify(
        title="Waktu Minum Obat!",
        message=f"Minumlah {medicine} dengan dosis {dose}",
        timeout=10
    )
