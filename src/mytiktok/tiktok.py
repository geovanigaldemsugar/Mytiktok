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

    def __init__(self, email:str, password:str, headless:bool = True) -> None:

        self._email = email
        self._password = password
        self.__validate_email_and_password(email, password)

        self._driver = Base(headless=headless).driver() 
        self._wait = WebDriverWait(self._driver, 15)
        self._login = Login(self._email, self._password, self._driver)



    def search(self, search_term:str, amount:int|None = None, save:bool = False, save_folder:str|None = None, load_time:str = 10 ) -> Videos:
        """
        Searchs For TikTok Videos
        
        Args:
            search term (str): terms to search.
            accounts (list): terms to search.
            amounts (int): amount of videos to get
            save (bool): save urls to txt files
            save_path (str): path to save scrape urls  
            load_time (int): load time between each successive scroll          
    
        Returns:  
            Videos Object:
 
        """

        self.__validate_search(search_term, amount, save, save_folder, load_time)


        #login and Enter search item in field
        self._login.login()
        search = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'[data-e2e="search-user-input"]' )))
        search.send_keys(search_term)

        #click search button
        search_button =  self._wait.until(EC.element_to_be_clickable((By.XPATH,'//button[@data-e2e="search-box-button"]' )))
        self._driver.execute_script("arguments[0].click();", search_button)

        time.sleep(5)
        result =  self.__get_urls_base(save=save, save_path=save_folder, load_time=load_time, amnt=amount)
        self._driver.quit()
        
        return Videos(urls= result)
    
    def accounts(self, accounts:list[str], amount:int|None = None, save:bool = False, save_folder:str|None = None, load_time:int = 10):
        """
        Get Videos From TikTok Account
        
        Args:
            accounts (list): terms to search.
            amounts (int): amount of videos to get
            save (bool): save urls to txt files
            save_path (str): path to save scrape urls  
            load_time (int): load time between each successive scroll       
    
        Returns:  
            AccVideos Object:
 
        """
        self.__validate_accounts(accounts, amount, save, save_folder, load_time)
           
        urls_of_accounts= {}
        
        #go to account page, and scrape account video of links, save to dictionary 
        for acct in accounts:
 
            save_path =  os.path.join('Accounts', acct + '.txt')
            account_page = 'https://www.tiktok.com/' + acct
            
            self._login.login(page=account_page) 

            time.sleep(1)            

            if save and not os.path.exists(save_folder): 
                os.makedirs(save_folder)
            print(acct)
            urls  = self.__get_urls_base (save=save, save_path=save_folder,load_time=load_time, amnt = amount)
            urls_of_accounts[acct]  = urls
        
        #finished scraped now quitting
        self._driver.quit()

        return AccVideos(urls=urls_of_accounts)
        
    
    def __get_urls_base(self, save=False, save_path=None, load_time = 10, amnt = None):
        """
        scraping base fucntion for Url Class

        """

        urls = []
        prev_urls = 0 

        while True:        
            #scroll to page end to load videos
            scroll = self._wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body') ))
            scroll.send_keys(Keys.END)
            
            #Give time for elements to load 
            time.sleep(load_time)  

            #find link elements containing links
            link_elements = self._wait.until(EC.presence_of_all_elements_located((By.XPATH,  '//div[@class=" css-1as5cen-DivWrapper e1cg0wnj1"]//a')))
            posts = [element.get_attribute('href') for element in link_elements]

            #get urls of videos types only and save them
            for url in posts:
                media_type  = url.split('/')[-2]
                if media_type == 'video':
                    urls.append(url)

            cur_urls  = len(posts)

            print(f"Videos Found {len(urls)}")

            #check if there is no more videos to load, note tiktok lowers responses speed over usage, this result in there being more videos to load but links elements were check before there loaded
            if cur_urls == prev_urls:
                break
            
            #update
            prev_urls = cur_urls

            #limiter
            if amnt is not None and cur_urls >= amnt:
                #url scraped sometimes overshoots, im just getiing rid of excess data
                urls = urls[:amnt]
                break
        
        #save file
        if save:  
            # create directories in the path if they arent there
            dirpath = os.path.dirname(save_path)
            if dirpath != '' and not os.path.exists(dirpath):
                os.makedirs(dirpath)
            
            with open(save_path, 'w')   as urls_file:
                [urls_file.write(url + '\n') for url in urls]
                print('Saved To: ' +  save_path)
    
        return urls
          
    @property
    def email_and_password(self) -> str:
        return self._email, self._password

    @email_and_password.setter
    def email_and_password(self, email:str, password:str) -> None:
        self.__validate_email_and_password(email, password)
        self._email = email
        self._password = password



    @staticmethod
    def __validate_email_and_password(email:str, password:str) -> None:
        """
        Validates email and password.
        
        Args:
            email (str): The TikTok email to validate.
            password (str): The TikTok password to validate

        Raises:
            TypeError: If the email and/or password is not strings.
            ValueError: If the email and/or password is a empty string.
        
        """

        if not isinstance(email, str):
            raise TypeError(f'Email must be a string but {type(email).__name__} received') 
        
        if not  isinstance(password,str):
            raise TypeError(f'Password must be a string but {type(password).__name__} received') 
        
        if not email:
            raise ValueError('Email is empty please eneter your email')
        
        if not password:
            raise ValueError('Password is Empty please eneter your password')
        

    @staticmethod
    def __validate_path(path:str) -> None:
        """
            Validates the File Path
            
            Args:
            path: Folder path to validate.
            
            Raises:
                UrlInvalidError: If the URL is invalid.
                UrlMediaTypeError: If the media type is not a video.
            
        """
        if not isinstance(path, str) and path is not None:
            raise TypeError(f'Filename or path must be a string but {type(path).__name__} received ')
        
        path_valid  = pathvalidate.is_valid_filepath(file_path=path, check_reserved=True, platform='auto')

        if not path_valid:
            raise ValueError(f'Path format is Invalid {path}')
        
        if not path.endswith('txt'):
                    raise ValueError(f'FileName extention is invalid must end with .txt')
                
       

    def __validate_search(self, search_term:str, amount:int, save:bool, save_folder:str, load_time:int) -> None:
            """
                Validates the search function arguments
                
                Args:
                search_term (str): Search term to validate.
                path (str): Folder path to validate.
                amount (str): amount varaible to validate.
                save_path (str): save variable to validate.
                load_time (int): loadtime variable to validate.

                
                Raises:
                    TypeError: If params is of wrong type.
                    ValueError: If the params are of inappropiate value.
                
            """
            if not isinstance(search_term, str):
                raise TypeError(f'Search term must be a string but received {type(search_term).__name__}')
        
            if not search_term:
                raise ValueError('Search term is empty please eneter your password')
        
            if save_folder is not None:
                self.__validate_path(save_folder)      
    
            if not isinstance(amount, int) and  amount != None:
                raise TypeError(f'amount must be a integer or None but received {type(amount).__name__}')
            
            if not isinstance(save, bool):
                raise TypeError(f'save must be bool but received {type(save).__name__}')
            

            if not save_folder and (save == True and save_folder == None) :
                raise ValueError('save path is empty please enter a save path')

            if not isinstance(load_time, int):
                raise TypeError(f'save  must be integer but received {type(load_time).__name__}')
            
                      
            

            
    def __validate_accounts(self, accounts:list[str], amount:int, save:bool, save_folder:str, load_time:int) -> None:
            """
                Validates the search function arguments
                
                Args:
                accounts (list): accounts to get videos from
                amount (str): amount varaible to validate.
                path (str): Folder path to validate.
                save (bool): save variable to validate.
                load_time (int): loadtime variable to validate.

                
                Raises:
                    UrlInvalidError: If the URL is invalid.
                    UrlMediaTypeError: If the media type is not a video.
                
            """
            if not isinstance(accounts, list):
                raise TypeError(f'Accounts must be list but received {type(accounts).__name__}')
        
            if not accounts:
                raise ValueError('Accounts list is empty')

            if save_folder is not None:
                self.__validate_path(save_folder)      

            if not isinstance(amount, int) and amount != None:
                raise TypeError(f'amount must be a integer or None but received {type(amount).__name__}')
            
            if not isinstance(save, bool):
                raise TypeError(f'save must be bool but received {type(save).__name__}')
            
            if not isinstance(save_folder, str) and  save_folder != None:
                raise TypeError(f'Save path must be a string or None but received {type(save_folder).__name__}')

            if not save_folder and (save == True and save_folder == None) :
                raise ValueError('save path is empty please enter a save path')

            if not isinstance(load_time, int):
                raise TypeError(f'save  must be integer but received {type(load_time).__name__}')
            
                      
            

            
      
        

            
