from src.mytiktok import Tiktok
from dotenv import load_dotenv
import os


load_dotenv('my_env.env')
email  = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


search_term = '#JesusSaves #prayer'

#the package needs an account login details to create cookie sessions 
tiktok  = Tiktok(email=email, password=password)

#returns a videos object
videos  = tiktok.search(search_term=search_term,  amount=5,  save=True, save_folder = 'search_urls/urls.txt')
print(videos.info)
videos.download(folder_name='Test_search')


