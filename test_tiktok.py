from src.mytiktok import Tiktok
from dotenv import load_dotenv
import os
from src.mytiktok import helper

#load env variables in environment
load_dotenv(dotenv_path='my_env.env')

email  = os.getenv('EMAIL')
password = os.getenv('PASSWORD')



tiktok = Tiktok(headless=True, email=email, password=password)

videos = tiktok.search(search_term='#Jesus saves', amnt=4)
print(videos.info_list)

