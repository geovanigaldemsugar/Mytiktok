from selenium.webdriver.common.by import By
from .helper import Helper
from . import helper
from .exceptions import *
import time
import pickle


class Login():

    def __init__(self, email, password, driver):
        #  call the initializing logic from parent class base
        self.email  = email
        self.password = password
        self.cookies = helper.cookies_path
        self.driver  = driver
        # self.captcha  = False


    def _login(self, page = 'https://www.tiktok.com/'):
        captcha  = False

        if Helper.need_login():
            # print('need to Login')
            # print("No cookies found or has Expired!!")
            self.driver.get('https://www.tiktok.com/')
            time.sleep(2)

            email_phone_button = self.driver.find_elements(By.CSS_SELECTOR, '.css-17hparj-DivBoxContainer.e1cgu1qo0')[1]
            email_phone_button.click()

            time.sleep(2)
            login_with_email = self.driver.find_element(By.XPATH,'//a[@href="/login/phone-or-email/email"]')
            login_with_email.click()
            
            # Retry unitl we get captched  or user we detect wrong login info
    
            time.sleep(10)
            email_input = self.driver.find_element(By.XPATH,'//input[@placeholder="Email or username"]')
            email_input.send_keys(self.email)

            time.sleep(10)
            password_input = self.driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
            password_input.send_keys(self.password)

            time.sleep(2)
            login = self.driver.find_element(By.XPATH,'//button[@data-e2e="login-button"]' )
            login.click()
            
            time.sleep(2)
            captcha  = Helper.captcha_present(self.driver)

            time.sleep(20)
            if captcha:
                raise EncounteredCaptchaError()
                
            time.sleep(18)
            
            # print("creating cookies!!")
            #get cookies for next session without having to login

            with open(self.cookies, 'wb') as cookie_file:
                pickle.dump(self.driver.get_cookies(),  cookie_file)  
            
            #save screenshot
            # self.driver.save_screenshot('getcookies.png')


        # print('Session Cookies found!')

        # got to tiktok page
        self.driver.get(page)

        #get cookies previosuly saved
        cookies = pickle.load(open(self.cookies, "rb"))
        
        #load cookeies
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        #refresh page 
        self.driver.refresh()

        time.sleep(1)

        captcha = Helper.captcha_present(self.driver)

        if captcha:
            raise EncounteredCaptchaError()
        
        # print('Login Successfully')






    
    
    