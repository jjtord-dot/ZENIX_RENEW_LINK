import os
import time
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def solve_zenix():
    print("🚀 Starting Zenix Auto-Renew...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # Stealth settings para magmukhang tao
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = os.environ.get('ZENIX_RENEW_LINK')

    try:
        driver.get(url)
        print("✅ Page loaded.")
        wait = WebDriverWait(driver, 20)

        # 1. HANAPIN ANG CAPTCHA IMAGE
        captcha_img = wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
        time.sleep(2)
        captcha_img.screenshot("captcha.png")
        print("📸 Captcha captured!")

        # 2. OCR READING
        text = pytesseract.image_to_string(Image.open("captcha.png"))
        solved_code = "".join(text.split())
        print(f"🔍 OCR Result: {solved_code}")

        # 3. INPUT AT SUBMIT
        input_box = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        input_box.send_keys(solved_code)
        
        submit_btn = driver.find_element(By.TAG_NAME, "button")
        submit_btn.click()
        
        time.sleep(5)
        print("🎉 Process Finished!")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    solve_zenix()
