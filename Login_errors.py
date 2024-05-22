from src.mytiktok.base import Base
from src.mytiktok.login import Login
from src.mytiktok import helper
import time
import os

if helper.Helper._Helper__cookies_exist(helper.COOKIES_PATH):os.remove(helper.COOKIES_PATH)
driver = Base(headless=False).driver()
Login('geovaninotice@gmail.com', '0912838', driver)._login()
driver.quit()

# <div class="captcha_verify_bar sc-hSdWYo glOlPh"><div class="captcha_verify_bar--close CloseButton___StyledDiv-wbp0x6-0 hLjlmj"><a class="verify-bar-close sc-chPdSV PffVT" id="verify-bar-close" role="button" aria-label="Close" tabindex="1"><svg class="verify-bar-close--icon" width="20px" height="20px" viewBox="0 0 20 20" version="1.1" xmlns="http://www.w3.org/2000/svg"><g transform="translate(3.875000, 3.875000)" fill="#999" fill-rule="nonzero"><path d="M11.6087836,0.641216373 C11.7970721,0.829504871 11.7970721,1.13478084 11.6087836,1.32306934 L6.807,6.125 L11.6087836,10.9269307 C11.7970721,11.1152192 11.7970721,11.4204951 11.6087836,11.6087836 C11.4204951,11.7970721 11.1152192,11.7970721 10.9269307,11.6087836 L6.125,6.807 L1.32306934,11.6087836 C1.13478084,11.7970721 0.829504871,11.7970721 0.641216373,11.6087836 C0.452927876,11.4204951 0.452927876,11.1152192 0.641216373,10.9269307 L5.443,6.125 L0.641216373,1.32306934 C0.452927876,1.13478084 0.452927876,0.829504871 0.641216373,0.641216373 C0.829504871,0.452927876 1.13478084,0.452927876 1.32306934,0.641216373 L6.125,5.443 L10.9269307,0.641216373 C11.1152192,0.452927876 11.4204951,0.452927876 11.6087836,0.641216373 Z" id="Path"></path></g></svg></a></div><div class="captcha_verify_bar--title sc-eHgmQL dIqiVd"><div class="sc-kkGfuU hBJQyG">Drag the slider to fit the puzzle</div></div></div>


# Woorrrkks!!!