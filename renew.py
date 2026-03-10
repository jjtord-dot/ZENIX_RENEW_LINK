import os
import time
import pytesseract
from PIL import Image
import undetected_照顾_chromedriver as uc # Special driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def solve_zenix():
    print("🚀 Starting Ultimate No-Error Script...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless') # Takbo sa background
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Ginagaya ang totoong tao na browser
    driver = uc.Chrome(options=options, version_main=122) 

    url = os.environ.get('ZENIX_RENEW_LINK')

    try:
        driver.get(url)
        print(f"✅ Page loaded: {url}")
        
        # Mas mahabang wait para sa Cloudflare (25 seconds)
        wait = WebDriverWait(driver, 25)

        # 1. HANAPIN ANG CAPTCHA IMAGE
        # Gagamit ng flexible XPath para kahit magbago ang design, mahanap pa rin
        captcha_img = wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@src, 'captcha')] | //img[not(contains(@src, 'logo'))]")))
        
        # Siguraduhin na ang screenshot ay malinaw para sa OCR
        captcha_img.screenshot("captcha.png")
        print("📸 Captcha captured!")

        # 2. OCR READING (PAGBASA NG CODE)
        img = Image.open("captcha.png")
        raw_text = pytesseract.image_to_string(img)
        solved_code = "".join(raw_text.split()) # Alisin lahat ng spaces
        print(f"🔍 OCR Result: {solved_code}")

        if not solved_code:
            raise Exception("Hindi nabasa ang CAPTCHA. Retrying may be needed.")

        # 3. INPUT AT SUBMIT
        input_box = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        input_box.send_keys(solved_code)
        
        # Hanapin ang button na may text na 'Verify'
        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Verify')]")
        submit_btn.click()
        
        print("👆 Verify button clicked!")
        time.sleep(8) # Hintayin ang "Renewal Successful" message
        
        print("🎉 Process Finished! Check your dashboard.")

    except Exception as e:
        print(f"❌ Error: {e}")
        driver.save_screenshot("error_debug.png") # Screenshot kung bakit nag-error
    finally:
        driver.quit()

if __name__ == "__main__":
    solve_zenix()
