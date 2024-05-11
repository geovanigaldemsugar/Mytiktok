from .base import Base
from .login import Login
from .exceptions import *
from .helper import Helper
from .videos import Videos
from .account_videos import AccVideos
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pathvalidate

class Tiktok():

    def __init__(self, email = None, password = None, headless = False):

        self.email = email
        self.password = password

        if self.email is None:
            raise NoInputError(method='email')
        
        if self.password is None:
            raise NoInputError(method='password')

        email_is_str  = isinstance(self.email, str)
        password_is_str  = isinstance(self.password,str)

        if not email_is_str:
            raise EmailNotStringError()
        
        if not password_is_str:
            raise PasswordNotStringError()
    
         # get driver from base class, initailze variables
        self.driver = Base(headless=headless).driver() 
        self.wait = WebDriverWait(self.driver, 30)
        self.login = Login(self.email, self.password, self.driver)



    def search(self, search_term = None, save = False, save_path = None, load_time = 10, amnt = None):
        """
        Get video links from search, you can search with hashtags or video name, return a list of videos urls 
        
        """
        if search_term is None:
            raise NoInputError(method='search')
        
        search_is_str =  isinstance(search_term, str)

        if not search_is_str:
            raise SearchTermNotStringError()
        
        if save:
            if save_path is None:
                raise NoInputError(method='file_name')
            
            path_valid  = pathvalidate.is_valid_filepath(file_path=save_path, check_reserved=True, platform='auto')

            if not path_valid:
                raise PathInvalidError()


        #login and Enter search item in field
        self.login._login()
        search = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'[data-e2e="search-user-input"]' )))
        search.send_keys(search_term)

        #click search button
        search_button =  self.wait.until(EC.element_to_be_clickable((By.XPATH,'//button[@data-e2e="search-box-button"]' )))
        self.driver.execute_script("arguments[0].click();", search_button)

        time.sleep(5)

        result =  self.__get_urls_base(save=save, save_path=save_path, load_time=load_time, amnt=amnt)
        self.driver.quit()

        
        return Videos(urls= result)
    
    def accounts(self, accounts = None, load_time = 10, save = False, save_folder = 'accounts', amnt = None):
        """
        scrape video links from accounts, need to provide a list of account or use Helper func to get them from account.txt

        """   
        if accounts is None:
            raise NoInputError(method='account')
        
        accounts_is_list  =  isinstance(accounts, list)

        if not accounts_is_list:
            raise AccountsNotListError()
        
        for acct in accounts:

            if not  Helper.valid_account(acct):
                raise AccountInvalidError(acct)
                
        if save:
            if save_folder is None:
                raise NoInputError(method='file_name')
        
            path_valid  = pathvalidate.is_valid_filepath(file_path=save_folder, check_reserved=True, platform='auto')

            if not path_valid:
                raise PathInvalidError()

           
        urls_of_accounts= {}
        
        #go to account page, and scrape account video of links, save to dictionary 
        for acct in accounts:
 
            save_path =  os.path.join(save_folder, acct + '.txt')
            account_page = 'https://www.tiktok.com/' + acct
            
            self.login._login(page=account_page) 

            time.sleep(1)            

            if save and not os.path.exists(save_folder): 
                os.makedirs(save_folder)
            print(acct)
            urls  = self.__get_urls_base (save=save, save_path=save_path,load_time=load_time, amnt = amnt)
            # print(urls)
            urls_of_accounts[acct]  = urls
        
        #finished scraped now quitting
        self.driver.quit()
        print("All Accounts found!!")

        

        return AccVideos(acc_urls=urls_of_accounts)
        
    
    def __get_urls_base(self, save=False, save_path=None, load_time = 10, amnt = None):
        """
        scraping base fucntion for Url Class

        """

        urls = []
    
        prev_urls = 0 

        while True:
                    
            #scroll to page end to load videos
            scroll = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body') ))
            scroll.send_keys(Keys.END)
            
            #Give time for elements to load 
            time.sleep(load_time)  

            #find link elements containing links
            link_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,  '//div[@class=" css-1as5cen-DivWrapper e1cg0wnj1"]//a')))


            posts = [element.get_attribute('href') for element in link_elements]

            #get those links
            for url in posts:
                media_type  = url.split('/')[-2]
                if media_type == 'video':
                    urls.append(url)


            cur_urls  = len(posts)

            #update
            print(f"Videos Found {cur_urls}")

            #check if there is no  more videos to load, note tiktok lowers responses speed over usage, this result in there being more videos to load but links elements were check before there loaded
            if cur_urls == prev_urls:
                break

            prev_urls = cur_urls


            #limiter
            if amnt is not None and cur_urls >= amnt:
                #url scraped sometimes overshoots, im just getiing rid of excess data
                urls = urls[:amnt]
                break

        
        #save file
        if save:
            with open(save_path, 'w')   as urls_file:
                [urls_file.write(url + '\n') for url in urls]
                print('saved ' +  save_path)
    
        return urls
          
  

    
if __name__ == '__main__':
   pass

# login --> search --> parse --> return
# snaptik - download
 