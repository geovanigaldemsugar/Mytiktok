from selenium.webdriver.common.by import By
from selenium.common import exceptions
import time
import os
import pickle
import requests

captcha = False
dir_path  = os.path.dirname(__file__)
cookies_path  =  os.path.join(dir_path, 'Data', 'cookies.pkl')

class Helper():

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
            driver.find_element(By.XPATH , '//div[@class = "captcha_verify_bar sc-eHgmQL izFRfC"]')
            present  = True
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
    # print(Helper.need_login())
    print(Helper._Helper__cookies_exist(cookies_path))
    # print(Helper._Helper__cookies_expired(cookies_path))
    # print(Helper.get_accounts())
    # print(Helper.get_hashtags())
    # print(Helper.valid_account('@calebbpartain'))


    