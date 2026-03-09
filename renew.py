import os
import time
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def solve_zenix():
    options = Options()
    options.add_argument('--headless') # Takbo sa background
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = os.environ.get('ZENIX_RENEW_LINK')

    try:
        driver.get(url)
        time.sleep(5) # Wait sa pag-load

        # 1. Hanapin ang CAPTCHA box at picturan
        # Gagamit tayo ng screenshot ng buong page tapos i-crop o direct element screenshot
        captcha_element = driver.find_element(By.CLASS_NAME, "text-2xl") # Base sa video mo
        captcha_element.screenshot("captcha.png")

        # 2. Basahin ang text gamit ang OCR
        raw_text = pytesseract.image_to_string(Image.open("captcha.png"))
        solved_code = raw_text.replace(" ", "").strip()
        print(f"Solved Code: {solved_code}")

        # 3. I-type sa input box
        input_box = driver.find_element(By.XPATH, "//input[@type='text']")
        input_box.send_keys(solved_code)

        # 4. Click Verify button
        btn = driver.find_element(By.XPATH, "//button[contains(., 'Verify')]")
        btn.click()
        
        time.sleep(5)
        print("Renewal Process Finished!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    solve_zenix()
  
