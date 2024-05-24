from .base import Base
from .helper import Helper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import pathvalidate

class AccVideos():

    def __init__(self, urls:dict[list]) -> None:
        self._urls:dict[list] = urls
        self._video_ids:list[str] = None
        self.info:list[dict]  = None
        self._accounts:list[str] = None

        self.__validate_urls_and_set_info(urls) 


    def download(self, folder_name:str) -> None:
            """
            Downloads TikTok Videos
            
            Args:
                 folder_name: The folder name to save the videos to.            
           
             Raises:
                ValueError: If the Urls is invalid.
                TypeError: If the media type is not a video.
            
            """

            self.__validate_path(folder_name)
            
            driver = Base(headless=True).driver()
            

            for acct in self._accounts:      

                # download each video
                for url, video_id in zip(self._urls[acct], self._video_ids[acct]):

                    #go to tiktok video post
                    driver.get(url)
                    video_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//video[@preload="auto"]')))
                    download_link = video_element.get_attribute('src')
                    cookies = driver.get_cookies()

                    cookies_request = {}
                    for cookie in cookies:
                        cookies_request[cookie.get('name')] = cookie.get('value')


                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    
                    account_path  = os.path.join(folder_name, acct)

                    if not os.path.exists(account_path):
                        os.makedirs(account_path)
                    
                    file_name = os.path.join(account_path, video_id + '.mp4')

                    # make a request for video file
                    response = requests.get(download_link, stream=True, cookies=cookies_request)

                    # download video file with progress bar
                    Helper.download(response=response, filepath=file_name, title=video_id)

            driver.quit()

            return True

            
    @property
    def urls(self) -> dict[list[dict]]:
        return self._urls

    @urls.setter
    def urls(self, urls:dict) -> None:
        self.__validate_urls_and_set_info(urls)
        self._urls = urls
    
    @staticmethod
    def __validate_path(path:str) -> None:
        """
            Validates the File Path
            
            Args:
            path: File path to validate.
            
            Raises:
                ValueError: If the path is invalid.
                TypeError: path is not a string.
            
        """
        if not isinstance(path, str):
            raise TypeError(f'Filename or path must be a string but {type(path).__name__} received ')
        
        path_valid  = pathvalidate.is_valid_filepath(file_path=path, check_reserved=True, platform='auto')

        if not path_valid:
            raise ValueError('Path format is Invalid {path}')
   
      

    @staticmethod
    def __validate_urls(urls:dict) -> tuple[list[str], list[dict]]:
        """
        Validates the TikTok Urls for each account and returns the video ID and list of response info.
        
        Args:
            url (dict): dictonary containing the TikTok Urls to validate.
        
        Returns:
            tuple: A tuple containing the video ID and the response info.
        
        Raises:
            ValueError: If the URL is invalid.
            TypeError: If the media type is not a video.
        
        """

          
        if not isinstance(urls, dict):
            raise  TypeError(f'Urls must be of type dict but {type(urls).__name__} received') 
        
        if not urls:
            raise ValueError('Urls dictionary provided is empty')
        
        video_ids:dict[list[str]] = {}
        temp_ids:list[str] = []
        infos:list[str] = []
        account_info:list[dict] = {}
        urls_of_account:list[list] = []
        accounts:list  = urls.keys()

        for acct in accounts:
            # get the urls list of each account
            urls_of_account.append(urls.get(acct))

            if not isinstance(urls_of_account, list):
                raise TypeError(f'Urls must be of type list but {type(urls).__name__} received for account:{acct}') 
            
            if not urls:
                raise ValueError(f'Urls list provided is empty for account:{acct}')
                
        

        for acct, urls, in zip(accounts, urls_of_account):
            for index, url in enumerate(urls):
                try:
                    requests.get(url)

                except requests.exceptions.InvalidSchema:
                    raise ValueError(f'Url format provided is invalid index:{index} "{url}"')
                

                # validate tiktok urls
                video_id:str  = url.split('/')[-1]

                tik_https_request = 'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@tiktok/video/' + video_id
                tik_response  = requests.get(tik_https_request)

                if not tik_response.status_code == 200:
                     raise ValueError(f'Url is Invalid please check the tiktok url again Index:{index} "{url}"')
            
                media_type  = url.split('/')[-2]

                if media_type != 'video':
                    raise TypeError('Photo post link was provided but this Package only supports downloading videos post Index:{index} "{url}"')

                temp_ids.append(video_id)
                
                #get info 
                info = tik_response.json()
                infos.append(info)
                account_info[acct]  = infos

            # store the video ids
            video_ids[acct] = temp_ids
            temp_ids:list[str] = []


        return accounts, video_ids, account_info

    def __validate_urls_and_set_info(self, urls:dict) -> None:
        """
        Validates the Urls and sets the video ID's and Info's attributes.

        """
        self._accounts, self._video_ids, self.info = self.__validate_urls(urls)


