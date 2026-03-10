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
    print("🚀 Starting Super Ultimate Zenix Auto-Renew...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = os.environ.get('ZENIX_RENEW_LINK')

    try:
        driver.get(url)
        print("✅ Page loaded. Waiting for CAPTCHA...")
        
        # Maghintay ng hanggang 30 seconds para lumabas ang image
        wait = WebDriverWait(driver, 30)
        
        # Hanapin ang kahit anong image na hindi logo
        captcha_img = wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@src, 'captcha')] | //img[not(contains(@src, 'logo'))]")))
        
        time.sleep(3) # Siguraduhin na loaded ang image bago picturan
        captcha_img.screenshot("captcha.png")
        print("📸 Captcha screenshot saved.")

        # OCR Reading
        text = pytesseract.image_to_string(Image.open("captcha.png"))
        solved_code = "".join(text.split())
        print(f"🔍 OCR Result: {solved_code}")

        # Input Box handling
        input_box = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        input_box.send_keys(solved_code)
        
        # Submit Button
        submit_btn = driver.find_element(By.TAG_NAME, "button")
        submit_btn.click()
        
        print("👆 Verify button clicked!")
        time.sleep(10) # Hintayin ang response ng server
        
        print("🎉 Process Complete!")

    except Exception as e:
        print(f"❌ Error encountered: {e}")
        driver.save_screenshot("error_page.png") # Picture ng error
    finally:
        driver.quit()

if __name__ == "__main__":
    solve_zenix()
