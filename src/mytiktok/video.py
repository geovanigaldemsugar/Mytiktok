from .base import Base
from .exceptions import *
from .helper import Helper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import pathvalidate


class Video():

    def __init__(self, url:str) -> None:
        """
    Get info about a Tiktok Video  and can Download it
    
    Args:
        url (str): Link or Url of the tiktok Video Post.

    """
        self._url = url
        self._video_id = None
        self._info = None

        #validate url and get info

        
        self.__validate_url_and_set_info(url)
        

    def download(self, file_name:str) -> None:
        """
        Downloads TikTok Video
        
        Args:
            file_name: The file name and or with path to save the video to.
        
        Raises:
            ValueError: If the URL is invalid.
            TypeError: If the media type is not a video.
        
        """
        self.__validate_path(file_name)

        driver = Base(headless=True).driver()

        # #go to tiktok video post
        driver.get(self._url)
        video_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//video[@preload="auto"]')))
        download_link = video_element.get_attribute('src')
        cookies = driver.get_cookies()

        cookies_request = {}
        for cookie in cookies:
            cookies_request[cookie.get('name')] = cookie.get('value')
        
        # make a request for video file
        response = requests.get(download_link, stream=True, cookies=cookies_request)
        
        dirpath = os.path.dirname(file_name)
        if dirpath != '' and not os.path.exists(dirpath):
            os.makedirs(dirpath)
        
        # download video file with progress bar
        Helper.download(response=response, filepath=file_name, title=self._video_id)
        driver.quit()  
        
        # create a fresh instance incase of repeated use
        driver = Base(headless=True).driver()



    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url:str) -> None:
        self.__validate_url_and_set_info(url)
        self._url = url
    
    @staticmethod
    def __validate_path(path:str) -> None:
        """
            Validates the File Path
            
            Args:
            path: File path to validate.
            
            Raises:
                UrlInvalidError: If the URL is invalid.
                UrlMediaTypeError: If the media type is not a video.
            
        """
        if not isinstance(path, str):
            raise TypeError(f'Filename or path must be a string but {type(path).__name__} received ')
        
        path_valid  = pathvalidate.is_valid_filepath(file_path=path, check_reserved=True, platform='auto')

        if not path_valid:
            raise ValueError('Path format is Invalid {path}')
        
        if not path.endswith('mp4'):
            raise ValueError(f'FileName extention is invalid must end with .mp4')
        
      

    @staticmethod
    def __validate_url(url:str) -> tuple[str, dict]:
        """
        Validates the TikTok URL and returns the video ID and response info.
        
        Args:
            url (str): The TikTok URL to validate.
        
        Returns:
            tuple: A tuple containing the video ID and the response info.
        
        Raises:
            UrlInvalidError: If the URL is invalid.
            UrlMediaTypeError: If the media type is not a video.
        
        """

        

        if not isinstance(url, str):
            raise TypeError(f'URL must be a string but {type(url).__name__} received') 
        
        try:
            requests.get(url)

        except requests.exceptions.InvalidSchema:
            raise ValueError(f'Url format provided is invalid {url}')
        

        video_id  = url.split('/')[-1]
        tik_https_request = 'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@tiktok/video/' + video_id
        tik_response  = requests.get(tik_https_request)

        if not tik_response.status_code == 200:
            raise ValueError('Url is Invalid please check the tiktok url again "{url}"')
        
        media_type  = url.split('/')[-2]

        if media_type != 'video':
            raise TypeError('Photo post link was provided but this Package only supports downloading videos post "{url}"')
            
        #get info 
        info = tik_response.json()

        return video_id, info

    def __validate_url_and_set_info(self, url):
        """
        Validates the URL and sets the video ID and Info attributes.
        """
        self._video_id, self._info = self.__validate_url(url)

           
        

