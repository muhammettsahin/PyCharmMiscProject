import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.maximize_window()

# Siteye giriş
driver.get("https://bayi.adaoto.com.tr/web/b2b/search")
time.sleep(15)

# Giriş işlemleri
driver.find_element(By.NAME, "customercode").send_keys("DA161246")
driver.find_element(By.NAME, "username").send_keys("UFUK")
driver.find_element(By.NAME, "password").send_keys("161616")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(20)

# Ürün ara
uretici = driver.find_element(By.ID,"uretici")
time.sleep(5)
uretici.click()
uretici.send_keys("WAGENBURG AYDINLATMA")
time.sleep(60)

# Scroll alanı
scroll_area = driver.find_element(By.CLASS_NAME, "datatable-body")

# Veri listesi
data = []
stok_kodlari_seti = set()

for i in range(300):  # Maksimum 80 scroll (gerekiyorsa arttırılır)
    rows = driver.find_elements(By.CSS_SELECTOR, ".datatable-body-row")
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, ".datatable-body-cell")
        if len(cells) >= 16:
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
                    "Test11": cells[15].text.strip()

                })
    # Scroll biraz aşağıya
    driver.execute_script("arguments[0].scrollTop += 400;", scroll_area)
    time.sleep(2)

# Excel'e yaz
df = pd.DataFrame(data)
df.to_excel("WAGEN.xlsx", index=False)

driver.quit()
print(f"{len(data)} satır başarıyla kaydedildi.")