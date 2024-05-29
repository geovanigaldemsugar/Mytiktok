import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from . import helper

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
        self.INSTALL_INFO = helper.Helper.is_chrome_installed()
        print(self.INSTALL_INFO.get('installed'))
        if not self.INSTALL_INFO.get('installed'):
            helper.Helper.install_chrome()
                

        #define options
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox') #prevents slenium from not accessing system resources
        # options.add_argument(f'--proxy-server={proxy}')
        # options.add_argument(f'user-agent={random_ua}')
        options.binary_location = self.INSTALL_INFO.get('chrome') 
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-dev-shm-usage")  # Prevents crashes in Docker


        # set driver to headless mode
        if headless:
            options.add_argument('--headless=new')

        self.options = options

    def driver(self):

        service = Service(executable_path = self.INSTALL_INFO.get('driver'))
        self.driver = uc.Chrome( Service=service, use_subprocess=False, options = self.options)
        return self.driver
    


if __name__ == '__main__':
    pass