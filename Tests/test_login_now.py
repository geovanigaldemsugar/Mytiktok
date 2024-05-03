from src.mytiktok.base import Base
from src.mytiktok.login import Login
import time


driver = Base().driver()

Login('geovaninotice@gmail.com', 'Geovani9!', driver)._login()
time.sleep(20)
driver.quit()


# Woorrrkks!!!