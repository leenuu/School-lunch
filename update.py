from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import os 
import sys
import shutil
import subprocess
import ctypes
import zipfile
import urllib.request


def is_admin():
    try:
        return ctypes.windll.Shell32.IsUserAnAdmin()
    except:
        return False

def unzip(source_file, dest_path):
    with zipfile.ZipFile(source_file, 'r') as zf:
        zf.extractall(path=dest_path)
        zf.close()

path = ''
url = 'https://github.com/leenuu/School-lunch-and-school-schedule/blob/master/update.txt'
ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}
req_html = requests.get(url, headers=header)
html = req_html.text
soup = BeautifulSoup(html,'html.parser')


if int(soup.find('div', class_='Box-body p-0 blob-wrapper data type-text').find('td', id='LC1').get_text()) == 1:
    if is_admin():
        pass
    else:
        # Re-run the program with admin rights
        ctypes.windll.Shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    print('update')
    url = 'https://github.com/leenuu/food_sd/archive/master.zip'
    urllib.request.urlretrieve(url,'update.zip')
    unzip(os.getcwd() + '/update.zip', os.getcwd())
    os.remove(os.getcwd() + '/update.zip')





