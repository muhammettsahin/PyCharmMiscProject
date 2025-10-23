import tkinter as tk
from tkinter import ttk
import json
import os


CONFIG_FILE = "config.json"

# =====================  SEKMELER  =====================





# =====================  GİRİŞ EKRANI  =====================
def kaydet_ve_baslat():
    secili_sekme = combo_sekme.get()

    if not secili_sekme:
        lbl_message.config(text="Lütfen tüm alanları doldurun!", fg="red")
        return

    # Bilgileri config.json'a kaydet
    config = {

        "sekme": secili_sekme
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

    lbl_message.config(text="Başlatılıyor...", fg="green")
    root.after(1000, root.destroy)  # pencereyi kapat


root = tk.Tk()
root.title("KF1500")
root.geometry("300x250")



tk.Label(root, text="Çalıştırılacak Sekme:").pack(pady=5)
combo_sekme = ttk.Combobox(root, values=[
    "Martaş",
    "Dinamik",
    "Sekme 3",  # MGA buraya bağlı
    "Sekme 4",
    "Sekme 5"
])
combo_sekme.pack()

tk.Button(root, text="Çalıştır", command=kaydet_ve_baslat).pack(pady=10)

lbl_message = tk.Label(root, text="")
lbl_message.pack()

root.mainloop()


# =====================  SEÇİLEN SEKMEYİ ÇALIŞTIR  =====================
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    secili_sekme = config["sekme"]

    if secili_sekme == "Martaş":
        import arama_mga
    elif secili_sekme == "Dinamik":
        import arama_dinamik
    elif secili_sekme == "BSG":
        import arama_bsg


else:
    print("Config dosyası bulunamadı!")
