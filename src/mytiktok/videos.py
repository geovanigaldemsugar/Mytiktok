from .base import Base
from .exceptions import *
from .helper import Helper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich.live import Live
from rich.text import Text
import requests
import os
import pathvalidate


class Videos():

    def __init__(self, urls:list[str]) -> None:
        self._urls = urls
        self._video_ids = None
        self.info = None
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
            
            # download each video
            for url,video_id in zip(self._urls, self._video_ids):

                
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
                    
                file_name = os.path.join(folder_name, video_id + '.mp4')

                # make a request for video file
                response = requests.get(download_link, stream=True, cookies=cookies_request)

                # download video file with progress bar
                Helper.download(response=response, filepath=file_name, title=video_id)

            driver.quit()
    
    

    @property
    def urls(self) -> list:
        return self._urls

    @urls.setter
    def urls(self, urls:list) -> None:
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
    def __validate_urls(urls:list) -> tuple[list[dict], list[dict]]:
        """
        Validates the TikTok URL and returns the video ID and list of response info.
        
        Args:
            url (list): the TikTok Urls to validate.
        
        Returns:
            tuple: A tuple containing the video ID and the response info.
        
        Raises:
            ValueError: If the URL is invalid.
            TypeError: If the media type is not a video.
        
        """

        if not isinstance(urls, list):
            raise TypeError(f'Urls must be of type list but {type(urls).__name__} received') 
        
        if not urls:
            raise ValueError('Urls list provided is empty')
            
        video_ids:list[dict] = []
        infos:list[dict] = []

        for index, url in enumerate(urls):
                    
            try:
                requests.get(url)

            except requests.exceptions.InvalidSchema:
                raise ValueError(f'Url format provided is invalid index:{index} "{url}"')
            
            # validate tiktok urls
            video_id  = url.split('/')[-1]

            tik_https_request = 'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@tiktok/video/' + video_id
            tik_response  = requests.get(tik_https_request)

            if  not tik_response.status_code == 200:
                raise ValueError(f'Url is Invalid please check the tiktok url again Index:{index} "{url}"')
            
            media_type  = url.split('/')[-2]

            if media_type != 'video':
                raise TypeError('Photo post link was provided but this Package only supports downloading videos post Index:{index} "{url}"')

            video_ids.append(video_id)

            #get info 
            info = tik_response.json()
            infos.append(info)

        return video_ids, infos

    def __validate_urls_and_set_info(self, urls) -> None:
        """
        Validates the Urls and sets the video ID's and Info's attributes.

        """
        self._video_ids, self.info = self.__validate_urls(urls)

    def __videos_stylized_text(self, amount:int, total:int) -> Text:
        text = Text(f'Downloading ', style= 'bold black on white') 
        text.append(f'{amount}', style='white on black')
        text.append(' of ', style= 'purple') 
        text.append(f'{total}', style= 'cyan')

           
        

            

