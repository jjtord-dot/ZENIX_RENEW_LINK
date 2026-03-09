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
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = os.environ.get('ZENIX_RENEW_LINK')

    try:
        driver.get(url)
        # Maghintay ng hanggang 20 seconds para lumabas ang page
        wait = WebDriverWait(driver, 20)

        # 1. HANAPIN ANG CAPTCHA IMAGE
        # Susubukan nating hanapin ang image mismo
        captcha_img = wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'captcha')] | //div[contains(@class, 'Verify')]//img")))
        
        # Kunin ang screenshot ng CAPTCHA
        captcha_img.screenshot("captcha.png")
        print("Captcha screenshot saved.")

        # 2. OCR READING
        raw_text = pytesseract.image_to_string(Image.open("captcha.png"))
        solved_code = "".join(raw_text.split()) # Mas malinis na pagtanggal ng spaces
        print(f"Solved Code: {solved_code}")

        # 3. TYPE SA INPUT BOX
        # Hahanapin natin yung box na may placeholder na 'Type the code'
        input_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder[contains(.,'code')]] | //input[@type='text']")))
        input_box.send_keys(solved_code)

        # 4. CLICK RENEW BUTTON
        renew_btn = driver.find_element(By.XPATH, "//button[contains(., 'Verify')]")
        renew_btn.click()
        
        time.sleep(5)
        print("Renewal request sent successfully!")

    except Exception as e:
        print(f"Bumagsak ang script: {e}")
        # Kukuha ng screenshot ng buong page para makita natin kung ano ang mali
        driver.save_screenshot("error_page.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    solve_zenix()
