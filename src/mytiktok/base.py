import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from . import helper
import os
class Base():
    
    """
    base class containing chrome driver object

    """

    def __init__(self, headless = False):
        
        #Guest mode to Be implmented when Guest Mode is added
        # user_agent = UserAgent()

        # Proxing to be Implemented when Guest Mode is added
        # random_ua = user_agent.random
        # proxy = 'http://185.217.143.96:80'

        # install chrome and chrome driver
        if not helper.INSTALLED:
            helper.Helper.install_chrome()
                

        #define options
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox') #prevents slenium from not accessing system resources
        # options.add_argument(f'--proxy-server={proxy}')
        # options.add_argument(f'user-agent={random_ua}')
        options.binary_location = '/home/geo/Desktop/Mytiktok/src/mytiktok/Data/chrome-linux64/chrome'
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-gpu')


        # set driver to headless mode
        if headless:
            options.add_argument('--headless=new')

        self.options = options

    def driver(self):

        service = Service(executable_path = helper.DRIVER)
        self.driver = uc.Chrome( Service=service, options = self.options)
        return self.driver
    


if __name__ == '__main__':
   pass

