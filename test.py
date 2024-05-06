from src.mytiktok import Tiktok


email = 'your_tiktok_email@gmail.com'
password = 'your_tiktok_password'
search_term = '#JesusSaves #prayer'

#the package needs an account login details to create cookie sessions 
tiktok  = Tiktok(email=email, password=password)

#returns a videos object
videos  = tiktok.search(search_term=search_term, amnt=14)
print(videos.info_list)
