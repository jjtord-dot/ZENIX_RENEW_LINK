import os
import time
import pytesseract
from PIL import Image
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def solve_zenix():
    print("🚀 Starting Zenix Auto-Renew (Undetected Mode)...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Siguraduhin na match ang version
    driver = uc.Chrome(options=options)
    url = os.environ.get('ZENIX_RENEW_LINK')

    try:
        driver.get(url)
        print(f"✅ Navigated to Zenix.")
        
        # Maghintay ng 30 seconds para lumabas ang page
        wait = WebDriverWait(driver, 30)

        # 1. HANAPIN ANG CAPTCHA
        # Mas pinalawak ang paghahanap para sa image
        captcha_img = wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@src, 'captcha')] | //img[not(contains(@src, 'logo'))]")))
        time.sleep(3) # Para fully loaded ang image
        captcha_img.screenshot("captcha.png")
        print("📸 Captcha image saved.")

        # 2. OCR READING (PAGBASA)
        img = Image.open("captcha.png")
        solved_code = pytesseract.image_to_string(img).strip()
        print(f"🔍 OCR Result: {solved_code}")

        # 3. INPUT AT I-SUBMIT
        # Hahanapin ang text box at button
        input_box = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "input")))
        input_box.send_keys(solved_code)
        
        submit_btn = driver.find_element(By.TAG_NAME, "button")
        submit_btn.click()
        
        print("👆 Verify button clicked! Waiting for server...")
        time.sleep(10)
        
        # Screenshot para sa proof ng tagumpay
        driver.save_screenshot("final_result.png")
        print("🎉 Process Complete!")

    except Exception as e:
        print(f"❌ Error encountered: {e}")
        driver.save_screenshot("error_debug.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    solve_zenix()
