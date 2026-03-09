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
    print("Starting Zenix Auto-Renew...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    # Stable Driver Setup
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = os.environ.get('ZENIX_RENEW_LINK')

    try:
        driver.get(url)
        print(f"Navigated to: {url}")
        
        # Maghintay ng 15 seconds para lumabas ang CAPTCHA
        wait = WebDriverWait(driver, 15)

        # 1. HANAPIN ANG CAPTCHA
        # Ito ang pinaka-accurate na paraan para mahanap ang image sa Zenix
        captcha_img = wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
        captcha_img.screenshot("captcha.png")
        print("Captcha screenshot captured.")

        # 2. BASAHIN ANG CODE
        text = pytesseract.image_to_string(Image.open("captcha.png"))
        solved_code = "".join(text.split()) # Tanggal spaces
        print(f"OCR Solved: {solved_code}")

        # 3. I-TYPE AT I-SUBMIT
        input_box = driver.find_element(By.TAG_NAME, "input")
        input_box.send_keys(solved_code)
        print("Code entered.")

        submit_btn = driver.find_element(By.TAG_NAME, "button")
        submit_btn.click()
        
        time.sleep(5) # Hintayin ang response
        print("Process complete! Check your Zenix dashboard.")

    except Exception as e:
        print(f"Error encountered: {e}")
        driver.save_screenshot("debug_error.png") # Para makita natin kung ano ang mali
    finally:
        driver.quit()

if __name__ == "__main__":
    solve_zenix()
