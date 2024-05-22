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
        self.cookies = helper.COOKIES_PATH
        self.driver  = driver
        # self.captcha  = False


    def _login(self, page = 'https://www.tiktok.com/'):
        captcha  = False

        if Helper.need_login(helper.COOKIES_PATH):
            # print('need to Login')
            # print("No cookies found or has Expired!!")
            self.driver.get('https://www.tiktok.com/')
            time.sleep(2)

            if not Helper.login_modal_present(self.driver):
                # print('testing')
                login_button = self.driver.find_element(By.XPATH, '//button[@id="header-login-button"]')
                login_button.click()

            # self.driver.save_screenshot('login.png')
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
            login = self.driver.find_element(By.XPATH,'//button[@data-e2e="login-button"]')
            login.click()
            

            time.sleep(2)
            captcha  = Helper.captcha_present(self.driver)
            
            # time.sleep(5)
            if captcha:
                raise EncounteredCaptchaError()

            time.sleep(5)

            self.driver.save_screenshot('login2.png')



            login_error = Helper.login_error(self.driver)
            error_text = login_error.get('error')
            print(error_text)
            print(login_error.get('found'))

            # check for the error
            if login_error.get('found'):

                if error_text == "Username or password doesn't match our records. Try again.":
                    raise LoginInvalidError('email or password')
                
                elif error_text == "Account doesn't exist":
                    raise LoginInvalidError('email and password')
                
                elif error_text == 'Maximum number of attempts reached. Try again later.':
                    raise LoginInvalidError('too many attempts') 

            
            
            # //span[@role="status"]
            # //*[@id="loginContainer"]/div[2]/form/div[3]/span
        
            # <span role="status">Username or password doesn't match our records. Try again.</span> Email/Username or password incorrect
            # <span role="status">Account doesn't exist</span> email ands password invalid
            
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






    
    
    