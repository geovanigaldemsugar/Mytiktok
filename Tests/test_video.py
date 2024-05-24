from src.mytiktok.video import Video
import time


url = 'https://www.tiktok.com/@inspiringfaith1/video/7361639338100428078'

start = time.time()
video  = Video(url = url)
video.download(file_name='Test_video/video/video.mp4')
stop = time.time()
print(round(stop - start, 2))
