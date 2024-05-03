from src.mytiktok.tiktok import Tiktok


tiktok  = Tiktok(email='geovaninotice@gmail.com', password= 'Geovani9!')
# print(tiktok.get_urls_from_search(search_term='#JesusSaves #prayer', amnt=14))
print(tiktok.get_urls_from_accounts(['@spreadthewordbro_'], save_folder='Tests/Test_accounts' ))



tiktok.get_urls_from_accounts


# wooorrkking