from src.mytiktok import Tiktok
from dotenv import load_dotenv
import os

load_dotenv('my_env.env')

email  = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

accounts  = [
'@calebbpartain',
'@dailychristmotives',
'@inspiringfaith1',
'@spreadthewordbro_',

]

#the package needs an account login details to create cookie sessions 
tiktok  = Tiktok(email=email, password=password)

#returns a videos object
videos  = tiktok.accounts(accounts=accounts, amount=3, save=True, save_folder='Accounts')
# print(videos._infos)

videos.download(folder_name='accounts_test')
