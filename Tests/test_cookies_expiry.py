import pickle
import time
from datetime import datetime


cookies =  pickle.load(open('cookies.pkl', 'rb'))       
date_format = "%b-%d-%Y" 



with open('cookie_names.txt', 'r') as cookie_names:
    important_cookies = cookie_names.read().splitlines()
    cookies_expiry_to_test  = []

    for cookie in cookies:
       name = cookie.get('name') 

       if name in important_cookies:
            expiry  = cookie.get('expiry')

            date = datetime.fromtimestamp(expiry)
            date = date.strftime(date_format)
            print(name)
            print(date)

            cookies_expiry_to_test.append(expiry)
            
    todays_date = time.time()
    
    earliest_expiry  = min(cookies_expiry_to_test)

    if earliest_expiry <= todays_date:
        expired = True
    else:
        expired = False

    print(expired)



# woorrrkkkking 