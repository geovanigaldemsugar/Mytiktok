from src.mytiktok import Tiktok
from dotenv import load_dotenv
import os
from src.mytiktok import helper
#load env variables in environment
load_dotenv(dotenv_path='my_env.env')

email  = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

# email = 'sadasdas@gmail.co,'
# password = '2efwfwfw'

print(helper.cookies_path)


# tiktok  = Tiktok(email=email, password=password).search(search_term='asdasda', amnt=4)
                                        