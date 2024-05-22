from .base import Base
from .exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os



class AccVideos():

    def __init__(self, acc_urls = {}):
        self.urls_dict = acc_urls
        self.urls_list = []
        info_list  = []
        video_id_list = []
        self.videos_ids_lists = []
        self.info_dict = {}
        
        acc_is_dic = isinstance(self.urls_dict, dict)

        if not acc_is_dic:
            raise UrlNotDictError()
        
        if not self.urls_dict:
            raise AccountDictEmptyError()
        

        self.accts_list  = self.urls_dict.keys()

        for acct in self.accts_list:

            urls = self.urls_dict.get(acct)
            url_is_list = isinstance(urls, list)

            if not url_is_list:
                raise UrlNotListError()

            if not urls:
                raise UrlsListEmptyError()

            self.urls_list.append(urls)

        for acct, urls, in zip(self.accts_list, self.urls_list):
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
        
                video_id_list.append(video_id)


                
                #get info 
                info = tik_response.json()
                info_list.append(info)
                self.info_dict[acct]  = info_list

            self.videos_ids_lists.append(video_id_list)


        # print(self.videos_ids_lists)

    def download(self, HD=False, load_time = 10, folder_name = 'accounts'):
            '''Download Videos in Bulk Using Snaptik Use Excessivly at Your Own Risk at Getting Ban IP '''

            driver = Base(headless=True).driver()

            index  = 0

            # print(self.accts_list)
            # print(self.urls_list)
            for acct, urls in zip(self.accts_list, self.urls_list):
               
                # download each video
                for url,video_id in zip(urls, self.videos_ids_lists[index]):

                    time.sleep(2)
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
                    
                    folder_path  = os.path.join(folder_name, acct)

                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    
                    file_name = os.path.join(folder_path, video_id + '.mp4')


                    with open(file_name, 'wb') as video:
                        for chunk in response.iter_content(chunk_size= 10 * 1024):
                            video.write(chunk)
                
                index += 1

            driver.quit()

            return True

            

