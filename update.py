from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import os 
import sys
import urllib.request
import time

start = time.time()
path = ''
url = 'https://github.com/leenuu/School-lunch-and-school-schedule/blob/master/update.txt'
ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}
req_html = requests.get(url, headers=header)
html = req_html.text
soup = BeautifulSoup(html,'html.parser')

if int(soup.find('div', class_='Box-body p-0 blob-wrapper data type-text').find('td', id='LC1').get_text()) == 1:
    print('update')
    url = 'https://github.com/leenuu/food_sd/archive/master.zip'
    urllib.request.urlretrieve(url,'update.zip')
end = time.time()

print(end - start)
    




