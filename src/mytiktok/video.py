from .base import Base
from .exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os
import pathvalidate


class Video():

    def __init__(self, url = None):
        self.url = url

        url_is_string = isinstance(self.url, str)

        if not url_is_string:
            raise UrlNotStringError()  
        
        if url is None:
            raise NoInputError(method='url')
        
        

        # validate tiktok url
        video_id  = url.split('/')[-1]
        tik_https_request = 'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@tiktok/video/' + video_id
        tik_response  = requests.get(tik_https_request)

        if tik_response.status_code == 400:
            raise UrlInvalidError(self.url)
        
        media_type  = url.split('/')[-2]

        if media_type != 'video':
            raise UrlMediaTypeError('Index {}'.format(url))
            
        #get info 
        self.info = tik_response.json()
           

    def download(self, file_name = None,  HD=False, load_time = 6):
        '''Download Videos in Bulk Using Snaptik Use Excessivly at Your Own Risk at Getting Ban IP '''
            
        if file_name is None:
            raise NoInputError(method='file_name')
        
        path_valid  = pathvalidate.is_valid_filepath(file_path=file_name, check_reserved=True, platform='auto')

        if not path_valid:
            raise PathInvalidError()
        
        if not file_name.endswith('mp4'):
            raise FileNameExtentionError()
            

        driver = Base(headless=True).driver()
            

        driver = Base(headless=True).driver()
        driver.get('https://snaptik.app/')

        time.sleep(2)
    

        input_url =  driver.find_element(By.XPATH, '//input[@id="url"]')
        input_url.send_keys(self.url)
        input_url.send_keys(Keys.ENTER)

        time.sleep(load_time)

        if HD:
            #hd links are dynamically generated 
            HD_button = driver.find_element(By.XPATH, '//button[@class="button btn-download-hd mt-3"]')
            HD_TOKEN =  HD_button.get_attribute('data-tokenhd')

            #send request to snaptik server
            https_request = 'https://snaptik.app/getHdLink.php?token=' + HD_TOKEN

            response = requests.get(https_request)
            error  = response.json().get('error')

            if error:
                raise HDDownloadError()
            
            download_link  = response.json().get('url')

        else:
            download_element  =  driver.find_element(By.XPATH, '//a[@class="button download-file"]')
            download_link  = download_element.get_attribute('href')


        driver.quit()
        
        response  = requests.get(download_link, stream=True)

        with open(file_name, 'wb') as video:
            for chunk in response.iter_content(chunk_size= 10 * 1024):
                video.write(chunk)

        return True


