from src.mytiktok import Tiktok
from dotenv import load_dotenv
import os


#load env variables in environment
load_dotenv(dotenv_path='my_env.env')

email  = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

tiktok  = Tiktok(email=email, password=password).get_urls_from_search(search_term='asdasda', amnt=4).download(folder_name='Test_videos')
                                                    