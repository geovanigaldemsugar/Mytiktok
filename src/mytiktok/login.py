from . import helper
from .exceptions import *
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pickle


class Login():

    def __init__(self, email:str, password:str, driver) -> None:
        self._email  = email
        self._password = password
        self._driver  = driver
        self._wait = WebDriverWait(self._driver, 10)
        self._COOKIES_PATH = helper.Helper.COOKIES_PATH
        self._DATA_PATH = helper.Helper.DATA_PATH


    def login(self, page:str = 'https://www.tiktok.com/') -> None:
        """
        Login to tiktok (load cookies) and/or save cookies.

        Args:
            page (str): Tiktok page to go to.
        Raises:
            EncounteredCaptchaError: if bot activity was detected.
            RuntimeError: login details was Inccorrect or somethign went wrong during login.

        
        """
        if self.__need_login(self._COOKIES_PATH):

            self._driver.get('https://www.tiktok.com/')
            time.sleep(2)

            if not self.__login_modal_present():
                login_button = self._wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@id="header-login-button"]')))
                login_button.click()

            time.sleep(2)
            email_phone_button = self._wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.css-17hparj-DivBoxContainer.e1cgu1qo0')))
            email_phone_button[1].click()

            time.sleep(2)
            login_with_email = self._wait.until(EC.visibility_of_element_located((By.XPATH,'//a[@href="/login/phone-or-email/email"]')))
            login_with_email.click()
            
            time.sleep(10)
            email_input = self._wait.until(EC.visibility_of_element_located((By.XPATH,'//input[@placeholder="Email or username"]')))
            email_input.send_keys(self._email)

            time.sleep(10)
            password_input = self._wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Password"]')))
            password_input.send_keys(self._password)

            time.sleep(2)
            login = self._wait.until(EC.visibility_of_element_located((By.XPATH,'//button[@data-e2e="login-button"]')))
            login.click()
     
            # wait for cpathca to load incase we were detected
            time.sleep(2)
        
            # give time to solve manually if decided to
            time.sleep(5) 
            if self.__captcha_present():
                raise EncounteredCaptchaError('Tiktok Triggered Captcha Cannot Proceed With Scraping')

            # give time for tiktok to check login details
            time.sleep(5)
            login_error, error_text = self.__login_error()
     
            if login_error:

                if error_text == "Username or password doesn't match our records. Try again.":
                    raise RuntimeError("Account does not exist please check login credentials")
                
                elif error_text == "Account doesn't exist":
                    raise RuntimeError('Email and password is incorrect please check login credentials')
                
                elif error_text == 'Maximum number of attempts reached. Try again later.':
                    raise RuntimeError("Tiktok detected too many login attempts please try again at a later time") 
                
                elif error_text == 'Something went wrong. Please try again later.':
                     raise RuntimeError('Something went wrong when attempting to login pLease try again later')

            #save cookies
            with open(self._COOKIES_PATH, 'wb') as cookie_file:
                pickle.dump(self._driver.get_cookies(),  cookie_file)  
            

        # got to tiktok page
        self._driver.get(page)

        #get previously saved cookies 
        cookies = pickle.load(open(self._COOKIES_PATH, "rb"))
        
        #load cookeies
        for cookie in cookies:
            self._driver.add_cookie(cookie)

        #refresh page 
        self._driver.refresh()

        time.sleep(1)
        if self.__captcha_present():
            raise EncounteredCaptchaError()
        



    def __need_login(self, file_path:str) -> bool:
        """Checks if login is needed """

        if not self.__cookies_exist(file_path) or self.__cookies_expired(file_path):
            need_login = True
        else:
            need_login = False
        
        return need_login

   
    def __cookies_exist(self, file_path:str) -> bool:
       """ Checks if Cookie file exists """
       return os.path.exists(file_path)
    

    def __cookies_expired(self, file_path:str) -> bool:
        """ Check if cookies has expired use cookie_names.txt to check for important cookies """

        cookies =  pickle.load(open(file_path, 'rb'))       
        
        #get cookies loaded back into a pyhton object 
        file_path_important_cookies  = os.path.join(self._DATA_PATH, 'cookie_names.txt')

        with open(file_path_important_cookies, 'r') as cookie_names:
            important_cookies = cookie_names.read().splitlines()
            cookies_expiry_to_test  = []

        for cookie in cookies:
            name = cookie.get('name') 

            if name in important_cookies:
                    expiry  = cookie.get('expiry')
                    cookies_expiry_to_test.append(expiry)
                    
            todays_date = time.time()
            
        earliest_expiry  = min(cookies_expiry_to_test)

        if earliest_expiry <= todays_date: 
            expired = True
        else:
            expired = False

        return expired

            
    def __captcha_present(self) -> bool:
        """ Checks if a Captcha is Present """
        try:
            captcha =   self._driver.find_element(By.XPATH , '//div[@class= "captcha_verify_bar sc-hSdWYo glOlPh"]')
            present  =  captcha.is_displayed()
        except exceptions.NoSuchElementException:
            present  = False

        return present
    

    def __login_modal_present(self) -> bool:
        """  Checks if loging modal is present on screen """
        try:
            modal = self._driver.find_element(By.XPATH, '//div[@id="loginContainer"]')
            present = modal.is_displayed()
        except exceptions.NoSuchElementException:
            present = False
        
        return present
    
    def __login_error(self) -> tuple[bool, str]:
        """ Checks  if  for Login responses from Tiktok """

        try:
            error_element = self._driver.find_element(By.XPATH, '//span[@role="status"]')  
            text = error_element.text
            found_error = True
        
        except exceptions.NoSuchElementException:
            text  = None
            found_error = False
        
        return  found_error, text
    
    