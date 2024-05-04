# MyTIkTok
### A Simple Python Package for Scarping and Downloading Tiktok Videos


## Installation

### Linux/Unix 
-  **`pip3 install mytiktok`**

### Windows
-  **`pip install mytiktok`**


## Example Usages
### Search for tiktok videos

```python 
from mytiktok import Tiktok


email = 'your_tiktok_email@gmail.com'
password = 'your_tiktok_password'
search_term = '#JesusSaves #prayer'

#the package needs an account login details to create cookie sessions 
tiktok  = Tiktok(email=email, password=password)

#returns a videos object
videos  = tiktok.search(search_term=search_term, amnt=14)
print(videos.info_list)

``` 
### Get Videos of an Accounts Video

```python 
from mytiktok import Tiktok


email = 'your_tiktok_email@gmail.com'
password = 'your_tiktok_password'

accounts  = [
'@calebbpartain',
'@dailychristmotives',
'@inspiringfaith1',
'@spreadthewordbro_',

]

#the package needs an account login details to create cookie sessions 
tiktok  = Tiktok(email=email, password=password)

#returns a videos object
videos  = tiktok.accounts(accounts=accounts, amnt=14)
print(video.info_list)

```
### Downloading Videos

#### Downloads videos via Search  or Accounts

```python         
videos.download(folder_name = 'Example_Folder') 
```

#### Download via Video

```python
from mytiktok.video import Video

url = 'https://www.tiktok.com/@calebbpartain/video/7363384781024906538'

video  = Video(url = url)
video.download(file_name='test.mp4')

```
#### Download via Videos Class
```python
from mytiktok.videos import Videos


urls  = [
'https://www.tiktok.com/@calebbpartain/video/72961sadsada4967404662062',
'https://www.tiktok.com/@calebbpartain/video/7314359034906234155',
'https://www.tiktok.com/@calebbpartain/video/7207942650564119854',
'https://www.tiktok.com/@calebbpartain/video/7363384781024906538',
]

videos  = Videos(urls = urls)
videos.download(folder_name='Test_videos')

```

## Limitations
- **Uses Chrome Instances**
- **Login attempts Frequently Fail**
- **Download atempts can fail from time to time**

#### If your planning to download in bulk ensure to save urls and use `Videos` class instead

> [!NOTE]
> If using this package headlessy, is important to your needs try running your script in a Docker

> [!IMPORTANT]
> Proxing has not been implemented so there is possiblity of snaptik.app blocking you and or slowing down connection but just dont download excessively, keep the rates low and you should be fine
