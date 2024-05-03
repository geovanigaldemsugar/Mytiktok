from src.mytiktok.videos import Videos


urls  = [
'https://www.tiktok.com/@calebbpartain/video/72961sadsada4967404662062',
'https://www.tiktok.com/@calebbpartain/video/7314359034906234155',
'https://www.tiktok.com/@calebbpartain/video/7207942650564119854',
'https://www.tiktok.com/@calebbpartain/video/7363384781024906538',
]

videos  = Videos(urls = urls)
videos.download(folder_name='Test_videos')


