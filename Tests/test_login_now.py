from src.mytiktok.base import Base
from src.mytiktok.login import Login
from dotenv import load_dotenv
import os


load_dotenv('my_env.env')
email  = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

driver = Base(headless =True).driver()

Login('geovaninotice@gmail.com', 'Geovani9!', driver).login()
driver.quit()


# Woorrrkks!!!