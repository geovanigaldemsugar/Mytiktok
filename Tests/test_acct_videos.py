from src.mytiktok.account_videos import AccVideos
import time

urls = { '@dailychristmotives':
[
"https://www.tiktok.com/@dailychristmotives/video/7327466953902247214",
"https://www.tiktok.com/@dailychristmotives/video/7363852564997147947"
]
 , '@inspiringfaith1':
[
"https://www.tiktok.com/@inspiringfaith1/video/7338271755309452575",
"https://www.tiktok.com/@inspiringfaith1/video/7348253651514772779"

] 
}

start = time.time()


videos  = AccVideos(urls = urls)
videos.download(folder_name='test_accounts_vids')

stop = time.time()
print(round(stop - start, 2))

