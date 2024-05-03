from src.mytiktok.video import Video



url = 'https://www.tiktok.com/@calebbpartain/video/7363384781024906538'

video  = Video(url = url)
video.download(file_name='test.mp4')