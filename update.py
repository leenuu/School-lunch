from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import os 
import sys
import urllib.request
import time

url = 'https://github.com/leenuu/School-lunch-and-school-schedule/blob/master/update.txt'
ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}
req_html = requests.get(url, headers=header)
html = req_html.text
soup = BeautifulSoup(html,'html.parser')

if int(soup.find('div', class_='Box-body p-0 blob-wrapper data type-text').find('td', id='LC1').get_text()) == 1:

    chunk_size = 1024
    url = 'https://github.com/leenuu/food_sd/archive/master.zip'
    with open('update.zip', "wb") as file:
        response = requests.get(url)              
        file.write(response.content)







