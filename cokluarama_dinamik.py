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
driver.find_element(By.NAME, "customercode").send_keys("DA348232")
driver.find_element(By.NAME, "username").send_keys("dell7pc")
driver.find_element(By.NAME, "password").send_keys("654321")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(10)

# Ürün ara
uretici = driver.find_element(By.ID, "uretici")
time.sleep(5)
uretici.click()
uretici.send_keys("KRAFTVOLL KLIMA KOMPRESORU")
time.sleep(10)

target = driver.find_element(By.XPATH, "//div[normalize-space(text())='KRAFTVOLL KLIMA KOMPRESORU']")
target.click()
time.sleep(60)

# Scroll alanı
scroll_area = driver.find_element(By.CLASS_NAME, "datatable-body")

# Veri listesi
data = []

for i in range(3):  # Maksimum 300 scroll (gerekiyorsa arttırılır)
    rows = driver.find_elements(By.CSS_SELECTOR, ".datatable-body-row")
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, ".datatable-body-cell")
        stok_kodu = cells[0].text.strip()
        if stok_kodu:  # sadece boş olmasın
            row_data = {
                "Stok Kodu": stok_kodu,
                "OEM Kodu": cells[1].text.strip(),
                "Marka": cells[2].text.strip(),
                "Ürün Adı": cells[3].text.strip(),
                "Açıklama": cells[4].text.strip()
            }

            # Test1 - Test16 alanları özel işlenir
            for j in range(5, 22):
                cell = cells[j]
                text = cell.text.strip()
                value = ""

                if text:
                    value = text
                else:
                    try:
                        img = cell.find_element(By.TAG_NAME, "img")
                        src = img.get_attribute("src").lower()

                        if "available" in src and "not" not in src:
                            value = "Var"
                        elif "notavailable" in src or "not-available" in src:
                            value = "Yok"
                        else:
                            value = ""
                    except:
                        value = ""

                row_data[f"Test{j - 4}"] = value

            data.append(row_data)

    # Scroll biraz aşağıya
    driver.execute_script("arguments[0].scrollTop += 400;", scroll_area)
    time.sleep(1)

# Excel'e yaz
df = pd.DataFrame(data)
df.to_excel("cokluaramadinamik161020252.xlsx", index=False)

driver.quit()
print(f"{len(data)} satır başarıyla kaydedildi.")
print("SRC:", src)
