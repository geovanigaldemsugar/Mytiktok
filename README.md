# MyTIkTok
### A Simple Python Package for Scarping and Downloading Tiktok Videos
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Google Chrome](https://img.shields.io/badge/Google%20Chrome-4285F4?style=for-the-badge&logo=GoogleChrome&logoColor=white)
![TikTok](https://img.shields.io/badge/TikTok-%23000000.svg?style=for-the-badge&logo=TikTok&logoColor=white)


## Installation
[![Downloads](https://static.pepy.tech/badge/mytiktok)](https://pepy.tech/project/mytiktok) 

### Linux/Unix 
-  **`pip3 install mytiktok`**

### Windows
-  **`pip install mytiktok`**

## Visual Output
The package itself uses undetected-chromedriver for web automation which controls whether the chrome instance to renders or not  hence the `headless` option. Using headless mode increases the chances of a captcha being raised and scraping process failing. So far in testing captcha is only noticed at `Login()`  but once login is successful cookies are created and you should be fine in successive usage of the package until the cookies expire.

So implementing Retries is important if you are planning on using this package for a project.

> [!NOTE]
> I recommend using `headless = True` after you've already passed Login and generated cookies, and after you can use `headless = False` but alternatively you can just always set `headless = True`




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
print(videos.info_dict)

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
video.download(file_name='video.mp4')

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
#### If you are planning to download in bulk ensure to save URLs and use the `Videos` class instead

## Limitations
- **Uses Chrome Instances**
- **Login attempts Frequently Fail**
- **Download attempts can fail from time to time**

## Issues
- [x] https://github.com/geovanigaldemsugar/Mytiktok/issues/1
- [ ] Slow

## Imporvements Coming Soon !
- [ ] Scraping Statistics
- [ ] Faster Scrape times
- [ ] Chrome Handling Done by the Package

 
> [!NOTE]
> If using this package with visual output is important to your needs try running your script in a Docker

> [!IMPORTANT]
> Proxing has not been implemented so there is a possibility of snaptik.app blocking you and or slowing down your connection but just don't download excessively, keep the rates low and you should be fine
