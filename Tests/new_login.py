from src.mytiktok.base import Base
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import pickle
from src.mytiktok.exceptions import EncountedCaptchaError

captcha  = False


def  captcha_present(driver):
    try:
        driver.find_element(By.XPATH , '//div[@class = "captcha_verify_bar sc-eHgmQL izFRfC"]')
        present  = True
    except exceptions.NoSuchElementException:
        present  = False

    return present

def captcha_appeared(driver):
    try:    
        test_element =  driver.find_element(By.XPATH, '//a[@data-e2e="nav-foryou"]')
        test_element.click()
        appeared = False

    except exceptions.ElementClickInterceptedException:
        print('not clickable')
        appeared = True

    except exceptions.ElementNotInteractableException:
        print('not interactable')
        appeared = True

    return appeared


driver = Base().driver()
wait = WebDriverWait(driver, 10)

driver.get('https://www.tiktok.com/')
time.sleep(2)

email_phone_button = driver.find_elements(By.CSS_SELECTOR, '.css-17hparj-DivBoxContainer.e1cgu1qo0')[1]
# print(email_phone_button)
email_phone_button.click()
login_with_email = driver.find_element(By.XPATH,'//a[@href="/login/phone-or-email/email"]')
# print(login_with_email)
login_with_email.click()

email = driver.find_element(By.XPATH,'//input[@placeholder="Email or username"]')
# print(email)
email.send_keys('geovticsadasdasqdasdas@gmail.com')

password = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
# print(password)
password.send_keys('asdsadsdasda!')

login = driver.find_element(By.XPATH,'//button[@data-e2e="login-button"]' )
print(login)
login.click()
time.sleep(2)

captcha  = captcha_present(driver) 
if captcha:
    raise EncountedCaptchaError()


print("creating cookies!!")
#get cookies for next session without having to login
# pickle.dump(driver.get_cookies(), open('cookies.pkl', 'wb'))      

#save screenshot
driver.save_screenshot('getcookies.png')

time.sleep(100)
driver.quit()