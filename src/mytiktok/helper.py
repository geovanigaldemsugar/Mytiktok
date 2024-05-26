import os
import requests
import platform
from zipfile import ZipFile
from tqdm import tqdm

class Helper():
    # Determine the directory where the package is installed
    PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(PACKAGE_PATH, 'Data')
    SYSTEM = platform.system()
    COOKIES_PATH =  os.path.join(DATA_PATH, 'cookies.pkl') 


    @staticmethod
    def download(response:requests.Response, filepath:str, title:str, color:str ='magenta', disable=False) -> None:
        """
        Download a file with progress Bar
        
        Args:
        Response : requests Response Object
        filepath (str) : file path to download to
        title (str) : title to display on the progress bar
        color (str) : color of progress bar
        disable (str): disable progress bar

        
        """


     
        format = '{l_bar}{bar}| {n_fmt}/{total_fmt}'

        # Send the GET request to download the video
        with  tqdm( desc=title, ascii=True, colour=color, total=int(response.headers.get('content-length')), unit_scale=True, bar_format=format, disable=disable,  dynamic_ncols=True) as progress_bar:
            with open(filepath,  "wb") as f:
                    # Write the video content to the file
                    for chunck in response.iter_content(10* 4024):
                        progress_bar.update(len(chunck))
                        f.write(chunck)
    
    @staticmethod
    def is_chrome_installed() -> dict['chrome':str, 'driver':str, 'installed':bool]:
        """       Checks if Chrome and Chromedriver is intalled and returns a dictionary containing thier PATHS, wither both was installed    """
        
        # check for os 
        if Helper.SYSTEM == 'Windows':
            chrome = os.path.join(Helper.DATA_PATH, 'chrome-win64', 'chrome.exe')
            driver = os.path.join(Helper.DATA_PATH, 'chromedriver-win64', 'chromedriver.exe')

        elif Helper.SYSTEM == 'Darwin':
            cpu_arch = platform.machine()
            # check for arm macs
            if cpu_arch  == 'arm64':
                chrome = os.path.join(Helper.DATA_PATH,'chrome-mac-arm64', 'Google Chrome for Testing.app' , 'Contents', 'Frameworks', 'Google Chrome for Testing Framework.framework','Versions','125.0.6422.78', 'Google Chrome for Testing Framework')
                driver = os.path.join(Helper.DATA_PATH, 'chromedriver-mac-arm64', 'chromedriver')
            else:
                chrome = os.path.join(Helper.DATA_PATH, 'chrome-mac-x64', 'Google Chrome for Testing.app' , 'Contents', 'Frameworks', 'Google Chrome for Testing Framework.framework','Versions','125.0.6422.78', 'Google Chrome for Testing Framework' , 'Google Chrome for Testing Framework')
                driver = os.path.join(Helper.DATA_PATH, 'chromedriver-mac-x64', 'chromedriver' )
        elif Helper.SYSTEM == 'Linux' :
            chrome = os.path.join(Helper.DATA_PATH, 'chrome-linux64', 'chrome')
            driver = os.path.join(Helper.DATA_PATH, 'chromedriver-linux64', 'chromedriver')


        # check if  chrome and driver are installed
        if os.path.exists(chrome) and os.path.exists(driver):
           installed = True
        else:
            installed = False


        return {'chrome':chrome, 'driver':driver, 'installed':installed }

    @staticmethod        
    def install_chrome() -> None:
        '''uses Chrome for testing since chrome browser binaries are easily avialable for WINDOWS'''

        # check for os 
        if Helper.SYSTEM == 'Windows':
            browser_url = 'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/win64/chrome-win64.zip'
            driver_url  =  'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/win64/chromedriver-win64.zip'
        
        elif Helper.SYSTEM == 'Darwin':
            cpu_arch = platform.machine()
            # check for arm macs
            if cpu_arch  == 'arm64':
                browser_url =  'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/mac-arm64/chrome-mac-arm64.zip'
                driver_url =  'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/mac-arm64/chromedriver-mac-arm64.zip'
            else:
                browser_url = 'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/mac-x64/chrome-mac-x64.zip'
                driver_url = 'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/mac-x64/chromedriver-mac-x64.zip'

        elif Helper.SYSTEM == 'Linux' :
            browser_url = 'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/linux64/chrome-linux64.zip'
            driver_url  = 'https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.76/linux64/chromedriver-linux64.zip'

        # parse the names from the urls and create thier paths
        browser_file_name = browser_url.split('/')[-1]
        driver_file_name = driver_url.split('/')[-1]
        browser_path  = os.path.join(Helper.DATA_PATH, browser_file_name)
        driver_path = os.path.join(Helper.DATA_PATH, driver_file_name)

        # download the compressed files
        browser_response = requests.get(browser_url, stream=True)
        driver_response = requests.get(driver_url,  stream= True)
        Helper.download(browser_response, browser_path, title='Downloading Chrome Browser', color='green')
        Helper.download(driver_response, driver_path, title='Downloading Chrome Driver', color='green' )
 
        # extract
        Helper.extract_zip_with_permissions(browser_path, Helper.DATA_PATH)
        Helper.extract_zip_with_permissions(driver_path, Helper.DATA_PATH)

        # remove downloaded files       
        os.remove(browser_path)
        os.remove(driver_path)

    @staticmethod
    def extract_zip_with_permissions(zip_path:str, extract_to:str) -> None:
        """
        Extract chrome and chrome driver  with their original executable permissions
        """
        with ZipFile(zip_path, 'r') as zip_file:
            # iterate over each file in zip file
            for member in zip_file.infolist():
                # extract
                extracted_path = zip_file.extract(member, extract_to)

                # Get original permissions
                perm = member.external_attr >> 16
                if perm:
                    os.chmod(extracted_path, perm)

  

    @staticmethod
    def valid_account(account:str) -> bool:
        """Checks If an account provided is Valid"""
        tik_http_request = 'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@tiktok/author/{}'.format(account)  
        response  = requests.get(tik_http_request)
        
        if response.status_code == 200:
            valid  = True
        else:
            valid = False

        return valid



    @staticmethod
    def get_hashtags(file_path = 'hashtags.txt'):
        #get file path of hastags file, nessesary to use as os will differ
        hastags =  open(file_path, 'r').read()

        return hastags
    

    @staticmethod
    def get_accounts(file_path  = 'accounts.txt') -> list[str]:
        """Returns a list of accounts from a file"""
        return open(file_path, 'r').read().split()    


# CONSTANTS


if __name__ == '__main__':
    # print(dir(Helper))
    # print(dir_path)
    # print(cookies_path)
    # print(Helper.need_login()) 
    # print(Helper._Helper__cookies_exist(cookies_path))
    # print(Helper._Helper__cookies_expired(cookies_path))
    # print(Helper.chrome_installed())
    if not Helper.is_chrome_installed().get('installed'): Helper.install_chrome()
    # print(Helper.get_accounts())
    # print(Helper.get_hashtags())
    # print(Helper.valid_account('@calebbpartain'))


    
