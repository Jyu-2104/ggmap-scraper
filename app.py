from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


def get_text_by_xpath(driver, xpath, default="Không có dữ liệu"):
    """Hàm lấy text từ XPath với xử lý ngoại lệ."""
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text.strip()
    except:
        return default

search_key = input(">> Input:  ")
keyword = search_key.replace(" ", "+")

crawl_url = f'https://www.google.com/maps/search/{keyword}'
driver.get(crawl_url)
time.sleep(5)


def scroll_and_collect():
    prev_count = 0
    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(3)
        list_result = driver.find_elements(By.CSS_SELECTOR, "a.hfpxzc")
        if len(list_result) == prev_count:
            break
        prev_count = len(list_result)
    return list_result

list_result = scroll_and_collect()
places = [link.get_attribute("href") for link in list_result]

print(f"\n🔹 Tổng số địa điểm tìm thấy: {len(places)}")
for idx, place_url in enumerate(places):
    print(f"{idx + 1}. {place_url}")

print("\n🔹 Đang lấy thông tin chi tiết...\n")
with open("google_maps_results.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Tên địa điểm", "Địa chỉ", "Số điện thoại", "Website"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for idx, place_url in enumerate(places):
        driver.get(place_url)
        time.sleep(5)
        
        name = get_text_by_xpath(driver, "//h1")
        address = get_text_by_xpath(driver, "//div[contains(@class, 'Io6YTe') and contains(@class, 'kR99db') and contains(@class, 'fdkmkc')]")
        phone = get_text_by_xpath(driver, "//button[contains(@data-item-id, 'phone')]")
        website = get_text_by_xpath(driver, "//div[contains(@class, 'ITvuef')]//div[contains(@class, 'Io6YTe') and contains(@class, 'kR99db') and contains(@class, 'fdkmkc')]")
        
        print(f"🔹 Địa điểm {idx + 1}:")
        print(f"   🏷️ Tên: {name}")
        print(f"   📍 Địa chỉ: {address}")
        print(f"   📞 Số điện thoại: {phone}")
        print(f"   🌐 Website: {website}\n")
        
        writer.writerow({"Tên địa điểm": name, "Địa chỉ": address, "Số điện thoại": phone, "Website": website})

driver.quit()
print("\n✅ Dữ liệu đã được lưu vào google_maps_results.csv")