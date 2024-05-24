import pickle
from datetime import datetime
from src.mytiktok import helper

cookies =  pickle.load(open(helper.COOKIES_PATH, 'rb'))       
date_format = "%b-%d-%Y" 


with open('cookies_analysis.txt', 'w') as text_file:

    for cookie in cookies:
        name =  cookie.get('name')
        expiry = cookie.get('expiry', 0)
        date = datetime.fromtimestamp(expiry)
        date = date.strftime(date_format)
        secure = cookie.get('secure')

        text_file.writelines([ 'name: ' + name  + '\n', 'expiry: ' +  str(date) + '\n', 'secure:' +  str(secure) + '\n\n'])
        

        print('name: ', cookie.get('name'))
        print('expiry: ', date)
        print('secure: ', cookie.get('secure'))






# name expiry secure