from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Tarayıcı başlat
driver = webdriver.Chrome()
driver.maximize_window()

# Siteye giriş
driver.get("https://online.martas.com.tr/web/b2b/search")
time.sleep(15)

# Giriş yap
driver.find_element(By.NAME, "customercode").send_keys("B102004")
driver.find_element(By.NAME, "username").send_keys("DORTAY")
driver.find_element(By.NAME, "password").send_keys("012345")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(5)


# Ürün ara
search_input = driver.find_element(By.ID, "searchInput")
search_input.send_keys("MGA-56315")
search_input.send_keys(Keys.ENTER)
time.sleep(5)

# Scroll ederek tüm verileri yükle
scroll_container = driver.find_element(By.CSS_SELECTOR, ".datatable-body")
last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)

for _ in range(50):  # 50 kez scroll etmeyi dene
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
    time.sleep(0.8)
    new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)
    if new_height == last_height:
        break
    last_height = new_height

# Tüm satırları al
rows = driver.find_elements(By.CSS_SELECTOR, ".datatable-body-row")
data = []
for row in rows:
    cells = row.find_elements(By.CSS_SELECTOR, ".datatable-body-cell")
    if len(cells) >= 20:
        data.append({
            "Stok Kodu": cells[0].text.strip(),
            "OEM Kodu": cells[1].text.strip(),
            "Marka": cells[2].text.strip(),
            "Ürün Adı": cells[3].text.strip(),
            "Açıklama": cells[4].text.strip(),
            #"Test1": cells[5].text.strip(),
            #"Test2": cells[6].text.strip(),
            #"Test3": cells[7].text.strip(),
            #"Test4": cells[8].text.strip(),
            "Test5": cells[9].text.strip(),
            "Test6": cells[10].text.strip(),
            "Test7": cells[11].text.strip(),
            "Test8": cells[12].text.strip(),
            "Test9": cells[13].text.strip(),
            "Test4": cells[14].text.strip(),
            "Test5": cells[15].text.strip(),
            "Test6": cells[16].text.strip(),
            "Test7": cells[17].text.strip(),
            "Test8": cells[18].text.strip(),
            "Test9": cells[19].text.strip(),
            "Liste Fiyatı": cells[20].text.strip()
        })

# Excel'e yaz
df = pd.DataFrame(data)
df.to_excel("martas_urun_listesi8.xlsx", index=False)

# Bitti
driver.quit()
print("Excel dosyası oluşturuldu: martas_urun_listesi.xlsx")
