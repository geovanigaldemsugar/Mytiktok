import pickle
import time


cookies =  pickle.load(open('cookies.pkl', 'rb'))       
# print(cookies)

#get cookies loaded back into a pyhton object 
with open('cookie_names.txt', 'r') as cookie_names:
    important_cookies = cookie_names.read().splitlines()
    # print(important_cookies)
    cookies_expiry_to_test  = []

for cookie in cookies:
    name = cookie.get("name") 
    print(name)

    if name in important_cookies:
            print(name)
            expiry  = cookie.get("expiry")
            cookies_expiry_to_test.append(expiry)
            
    todays_date = time.time()
    
    earliest_expiry  = min(cookies_expiry_to_test)

    if earliest_expiry <= todays_date: 
        expired = True
    else:
        expired = False
    print(expired)