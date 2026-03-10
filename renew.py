import os
import time
import pytesseract
from PIL import Image
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def solve_zenix():
    print("🚀 Starting Zenix Auto-Renew (Final Stable)...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Gagamit ng automatic driver fetcher para iwas version conflict
    driver = uc.Chrome(options=options)

    url = os.environ.get('ZENIX_RENEW_LINK')

    try:
        driver.get(url)
        print(f"✅ Page loaded: {url}")
        
        wait = WebDriverWait(driver, 25)

        # 1. HANAPIN ANG CAPTCHA
        captcha_img = wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@src, 'captcha')] | //img[not(contains(@src, 'logo'))]")))
        captcha_img.screenshot("captcha.png")
        print("📸 Captcha captured!")

        # 2. OCR READING
        img = Image.open("captcha.png")
        raw_text = pytesseract.image_to_string(img)
        solved_code = "".join(raw_text.split())
        print(f"🔍 OCR Result: {solved_code}")

        # 3. INPUT AT SUBMIT
        input_box = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        input_box.send_keys(solved_code)
        
        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Verify')]")
        submit_btn.click()
        
        print("👆 Verify button clicked!")
        time.sleep(10) 
        
        print("🎉 Renewal request completed.")

    except Exception as e:
        print(f"❌ Error encountered: {e}")
        driver.save_screenshot("error_debug.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    solve_zenix()
