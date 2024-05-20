from selenium.webdriver.common.by import By
from selenium.common import exceptions
import time
import os
import pickle
import requests
import platform
import subprocess
import distro
# import shutil

captcha = False
dir_path  = os.path.dirname(__file__)
DATA_PATH = os.path.join(dir_path, 'Data')
cookies_path  =  os.path.join(dir_path, 'Data', 'cookies.pkl')
CHROME_EXECUTABLE = os.path.join(dir_path)
SYSTEM = platform.system()

class Helper():
    @staticmethod
    def download_from_url(url, path):
        response  = requests.get(url, stream=True)

        with open(path, 'wb') as executable:
            for chunk in response.iter_content(chunk_size= 10 * 1024):
                executable.write(chunk)

    @staticmethod
    def chrome_installed():
        cmd = "where" if SYSTEM == "Windows" else "which"
        result = subprocess.run([cmd, "google-chrome"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exits = result.returncode == 0
        
        return exits


    def install_chrome():
        

        if SYSTEM == 'Windows':
            url = ''
            pass
        elif SYSTEM == 'Darwin':
            pass

        elif SYSTEM == 'Linux' :
            DISTRO = platform.freedesktop_os_release('ID LIKE')
            if DISTRO == 'debian':
                pass
            elif distro == 'fedora':
                pass
        
        # file_type = os.
            
        print('Downloading Chrome Executable')

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
    def need_login(file_path = cookies_path):

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
        file_path_important_cookies  = os.path.join( dir_path, 'Data', 'cookie_names.txt')

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


if __name__ == '__main__':
    # print(dir(Helper))
    # print(dir_path)
    # print(cookies_path)
    print(Helper.need_login()) 
    # print(Helper._Helper__cookies_exist(cookies_path))
    # print(Helper._Helper__cookies_expired(cookies_path))
    # print(Helper.chrome_installed())
    # print(Helper.get_accounts())
    # print(Helper.get_hashtags())
    # print(Helper.valid_account('@calebbpartain'))


    