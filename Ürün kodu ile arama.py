from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

driver = webdriver.Chrome()
driver.maximize_window()

# Siteye giriş
driver.get("https://online.martas.com.tr/web/b2b/search")
time.sleep(15)

# Giriş işlemleri
driver.find_element(By.NAME, "customercode").send_keys("B102004")
driver.find_element(By.NAME, "username").send_keys("DORTAY")
driver.find_element(By.NAME, "password").send_keys("012345")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(5)

# Ürün ara
search_input = driver.find_element(By.ID, "searchInput")
search_input.send_keys("MGA-56315")
search_input.send_keys(Keys.ENTER)
time.sleep(3)

# Scroll alanı
scroll_area = driver.find_element(By.CLASS_NAME, "datatable-body")

# Veri listesi
data = []
stok_kodlari_seti = set()

for i in range(80):  # Maksimum 80 scroll (gerekiyorsa arttırılır)
    rows = driver.find_elements(By.CSS_SELECTOR, ".datatable-body-row")
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, ".datatable-body-cell")
        if len(cells) >= 21:
            stok_kodu = cells[0].text.strip()
            if stok_kodu and stok_kodu not in stok_kodlari_seti:
                stok_kodlari_seti.add(stok_kodu)
                data.append({
                    "Stok Kodu": stok_kodu,
                    "OEM Kodu": cells[1].text.strip(),
                    "Marka": cells[2].text.strip(),
                    "Ürün Adı": cells[3].text.strip(),
                    "Açıklama": cells[4].text.strip(),
                    "Fiyat": cells[20].text.strip()
                })
    # Scroll biraz aşağıya
    driver.execute_script("arguments[0].scrollTop += 400;", scroll_area)
    time.sleep(1)

# Excel'e yaz
df = pd.DataFrame(data)
df.to_excel("martas_tam_liste1.xlsx", index=False)

driver.quit()
print(f"{len(data)} satır başarıyla kaydedildi.")