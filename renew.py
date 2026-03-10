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
    print("Starting Ultimate Zenix Auto-Renew...")
    options = Options()
    options.add_argument('--headless=new') # Updated headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    # Para hindi mahalata na bot
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = os.environ.get('ZENIX_RENEW_LINK')

    try:
        driver.get(url)
        print("Page opened. Waiting for elements...")
        
        wait = WebDriverWait(driver, 20)

        # 1. HANAPIN ANG CAPTCHA IMAGE (Mas matinding Filter)
        # Hahanapin ang kahit anong image na hindi logo
        captcha_img = wait.until(EC.visibility_of_element_located((By.XPATH, "//img[not(contains(@src, 'logo'))]")))
        captcha_img.screenshot("captcha.png")
        print("Captcha image saved.")

        # 2. OCR READING
        raw_text = pytesseract.image_to_string(Image.open("captcha.png"))
        solved_code = "".join(raw_text.split()) 
        print(f"OCR Result: {solved_code}")

        # 3. TYPE AND SUBMIT
        # Hahanapin ang text box at ang tanging button sa page
        input_box = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "input")))
        input_box.send_keys(solved_code)
        
        submit_btn = driver.find_element(By.TAG_NAME, "button")
        submit_btn.click()
        
        print("Verify button clicked. Waiting for confirmation...")
        time.sleep(10) # Mas matagal na hintay para sa server response
        
        # Screenshot para sa proof ng success
        driver.save_screenshot("result.png")
        print("Check result.png in artifacts if enabled.")

    except Exception as e:
        print(f"Bumagsak: {e}")
        driver.save_screenshot("error_debug.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    solve_zenix()
