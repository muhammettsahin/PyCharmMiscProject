import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

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
uretici = driver.find_element(By.ID,"uretici")
time.sleep(5)
uretici.click()
uretici.send_keys("MGA RADYATÖR")
time.sleep(3)

# Scroll alanı
scroll_area = driver.find_element(By.CLASS_NAME, "datatable-body")

# Veri listesi
data = []
stok_kodlari_seti = set()

for i in range(300):  # Maksimum 80 scroll (gerekiyorsa arttırılır)
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
                    "Test1": cells[5].text.strip(),
                    "Test2": cells[6].text.strip(),
                    "Test3": cells[7].text.strip(),
                    "Test4": cells[8].text.strip(),
                    "Test5": cells[9].text.strip(),
                    "Test6": cells[10].text.strip(),
                    "Test7": cells[11].text.strip(),
                    "Test8": cells[12].text.strip(),
                    "Test9": cells[13].text.strip(),
                    "Test10": cells[14].text.strip(),
                    "Test11": cells[15].text.strip(),
                    "Test12": cells[16].text.strip(),
                    "Test13": cells[17].text.strip(),
                    "Test14": cells[18].text.strip(),
                    "Test15": cells[19].text.strip(),
                    "Test16": cells[20].text.strip()
                })
    # Scroll biraz aşağıya
    driver.execute_script("arguments[0].scrollTop += 400;", scroll_area)
    time.sleep(1)

# Excel'e yaz
df = pd.DataFrame(data)
df.to_excel("mga-rad.xlsx", index=False)

driver.quit()
print(f"{len(data)} satır başarıyla kaydedildi.")