from selenium.webdriver.common.by import By
from selenium.common import exceptions
import time
import os
import pickle
import requests
import platform
from dlbar import DownloadBar
from zipfile import ZipFile
import patoolib

class Helper():
    
    @staticmethod
    def is_chrome_installed():
        '''Checks if Chrome and Chromedriver is intalled and returns a dictions containing thier PATHS, wither both was installed'''
        
        # check for os 
        if SYSTEM == 'Windows':
            folder_names = ('chrome-mac-arm64', 'chromedriver-mac-arm64')

        elif SYSTEM == 'Darwin':
            cpu_arch = platform.machine()
            # check for arm macs
            if cpu_arch  == 'arm64':
                folder_names = ('chrome-mac-arm64', 'chromedriver-mac-arm64')
            else:
                folder_names = ('chrome-mac-x64', 'chromedriver-mac-x64' )

        elif SYSTEM == 'Linux' :
            folder_names = ('chrome-linux64','chromedriver-linux64')

        chrome =  '/home/geo/Desktop/Mytiktok/src/mytiktok/Data/chrome-linux64/chrome'
        driver = os.path.join(DATA_PATH, folder_names[1], 'chromedriver')


        if os.path.exists(chrome) and os.path.exists(driver):
           installed = True
        else:
            installed = False


        return {'chrome':chrome, 'driver':driver, 'installed':installed }

            
    def install_chrome():
        '''uses Chrome for testing since chrome browser binaries are easily avialable for WINDOWS'''

        # check for os 
        if SYSTEM == 'Windows':
            browser_url = 'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/win64/chrome-win64.zip'
            driver_url  =  'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/win64/chromedriver-win64.zip'
        
        elif SYSTEM == 'Darwin':
            cpu_arch = platform.machine()
            # check for arm macs
            if cpu_arch  == 'arm64':
                browser_url =  'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/mac-arm64/chrome-mac-arm64.zip'
                driver_url =  'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/mac-arm64/chromedriver-mac-arm64.zip'
            else:
                browser_url = 'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/mac-x64/chrome-mac-x64.zip'
                driver_url = 'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/mac-x64/chromedriver-mac-x64.zip'

        elif SYSTEM == 'Linux' :
            browser_url = 'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/linux64/chrome-linux64.zip'
            driver_url  = '	https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/linux64/chromedriver-linux64.zip'

        # parse the names from the urls and create thier paths
        browser_file_name = browser_url.split('/')[-1]
        driver_file_name = driver_url.split('/')[-1]
        browser_path  = os.path.join(DATA_PATH, browser_file_name)
        driver_path = os.path.join(DATA_PATH, driver_file_name)

        # download the compressed files
        download_bar = DownloadBar()
        download_bar.download(url=browser_url, dest=browser_path, title='Downloading Chrome Browser')
        download_bar.download(url=driver_url, dest=driver_path, title='Downloading Chrome Driver')


        Helper.extract_zip_with_permissions(browser_path, DATA_PATH)
        Helper.extract_zip_with_permissions(driver_path, DATA_PATH)


        # patoolib.extract_archive(browser_path, outdir=DATA_PATH)
        # patoolib.extract_archive(driver_path, outdir=DATA_PATH)

        # extract chrome and driver zip files
        # for zip_file_path in (browser_path, driver_path):
        #     with ZipFile(zip_file_path, 'r') as zip_file:
        #         zip_file.extractall(DATA_PATH)
        #         zip_file.close()

        # remove downloaded files
       
        os.remove(browser_path)
        os.remove(driver_path)

    @staticmethod
    def extract_zip_with_permissions(zip_path, extract_to):
        with ZipFile(zip_path, 'r') as zip_file:
            # iterate over each file in zip file
            for member in zip_file.infolist():
                # extract
                extracted_path = zip_file.extract(member, extract_to)

                # Get original permissions
                perm = member.external_attr >> 16
                if perm:
                    os.chmod(extracted_path, perm)

    @staticmethod
    def login_modal_present(driver):
        try:
            modal = driver.find_element(By.XPATH, '//div[@id="loginContainer"]')
            present = modal.is_displayed()
        except exceptions.NoSuchElementException:
            present = False
        
        return present
    def login_error(driver):
        try:
            error_element = driver.find_element(By.XPATH, '//span[@role="status"]')  
            text = error_element.text
            found_error = True
        
        except exceptions.NoSuchElementException:
            text  = None
            found_error = False
        
        return {'found':found_error, 'error':text}

    @staticmethod
    def valid_account(account):
        tik_http_request = 'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@tiktok/author/{}'.format(account)  
        response  = requests.get(tik_http_request)
        
        if response.status_code == 200:
            valid  = True
        else:
            valid = False

        return valid

    @staticmethod
    def captcha_present(driver):
        try:
            captcha =   driver.find_element(By.XPATH , '//div[@class= "captcha_verify_bar sc-hSdWYo glOlPh"]')
            # captcha =   driver.find_element(By.XPATH , '//div[@class = "captcha_verify_bar sc-eHgmQL izFRfC"]')
            #  class="captcha_verify_bar sc-hSdWYo glOlPh"
            present  =  captcha.is_displayed()
        except exceptions.NoSuchElementException:
            present  = False

        return present

    @staticmethod
    def get_hashtags(file_path = 'hashtags.txt'):
        #get file path of hastags file, nessesary to use as os will differ
        hastags =  open(file_path, 'r').read()

        return hastags
    
    @staticmethod
    def need_login(file_path):

        if not Helper.__cookies_exist(file_path) or Helper.__cookies_expired(file_path):
            need_login = True
        else:
            need_login = False
        
        return need_login
    @staticmethod
    def get_accounts(file_path  = 'accounts.txt'):
        return open(file_path, 'r').read().split()    
    

    @staticmethod
    def __cookies_expired(file_path):
        ''' check if cookies has expired use cookie_names.txt to check for important cookies'''
        cookies =  pickle.load(open(file_path, 'rb'))       
        
        #get cookies loaded back into a pyhton object 
        file_path_important_cookies  = os.path.join(DIR_PATH, 'Data', 'cookie_names.txt')

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

    
    @staticmethod
    def __cookies_exist(file_path):
       return os.path.exists(file_path)
            
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

# CONSTANTS
captcha = False
DIR_PATH  = os.path.dirname(__file__)
DATA_PATH = os.path.join(DIR_PATH, 'Data')
COOKIES_PATH =  os.path.join(DATA_PATH, 'cookies.pkl')
SYSTEM = platform.system()
RESULT = Helper.is_chrome_installed()
CHROME = RESULT.get('chrome')
DRIVER = RESULT.get('driver')
INSTALLED = RESULT.get('installed')

if __name__ == '__main__':
    # print(dir(Helper))
    # print(dir_path)
    # print(cookies_path)
    # print(Helper.need_login()) 
    # print(Helper._Helper__cookies_exist(cookies_path))
    # print(Helper._Helper__cookies_expired(cookies_path))
    # print(Helper.chrome_installed())
    if not INSTALLED: Helper.install_chrome()
    # print(Helper.get_accounts())
    # print(Helper.get_hashtags())
    # print(Helper.valid_account('@calebbpartain'))


    