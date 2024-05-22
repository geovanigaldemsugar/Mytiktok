from .base import Base
from .exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os
import pathvalidate



class Videos():

    def __init__(self, urls = []):
        self.urls = urls
        url_list = isinstance(self.urls, list)
        self.info_list  = []
        self.video_id_list = []

        if not url_list:
            raise UrlNotListError()
        
        if not self.urls:
            raise UrlsListEmptyError()
        
        
        for index, url in enumerate(urls):
            # validate tiktok urls
            video_id  = url.split('/')[-1]

            tik_https_request = 'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@tiktok/video/' + video_id
            tik_response  = requests.get(tik_https_request)

            if tik_response.status_code == 400:
                raise UrlInvalidError(url= 'Index {}, {}'.format(index, url) )
            
            media_type  = url.split('/')[-2]

            if media_type != 'video':
                raise UrlMediaTypeError('Index {}, {}'.format(index, url))
    
            self.video_id_list.append(video_id)

            
            #get info 
            info = tik_response.json()
            self.info_list.append(info)

    def download(self, folder_name = None,  HD=False, load_time = 10):
            '''Download Videos in Bulk Using Snaptik Use Excessivly at Your Own Risk at Getting Ban IP '''

            driver = Base(headless=True).driver()
            

            if folder_name is None:
                raise NoInputError(method='folder_name')

            path_valid  = pathvalidate.is_valid_filepath(file_path=folder_name, check_reserved=True, platform='auto')

            if not path_valid:
                raise PathInvalidError()
            
            
            # download each video
            for url,video_id in zip(self.urls, self.video_id_list):

                
                #got to snaptik
                driver.get('https://snaptik.app/')
                time.sleep(2)


                #Enter url 
                input_url = driver.find_element(By.XPATH, '//input[@id="url"]')
                input_url.send_keys(url)
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

                
                response  = requests.get(download_link, stream=True)


                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                file_name = os.path.join(folder_name, video_id + '.mp4')

                with open(file_name, 'wb') as video:
                    for chunk in response.iter_content(chunk_size= 10 * 1024):
                        video.write(chunk)
            
            driver.quit()
    
            return True

            

