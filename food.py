from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import datetime as dy
import requests
import tkinter
import tkinter.font
import urllib.request
import cv2
import os 


data = list()
text_data = '\n'
text = ''
text_ = ''
er = 0

url = f'http://jeil.jje.hs.kr/jeil-h/food/2020/{dy.datetime.today().month}/{dy.datetime.today().day}/lunch'
# url = "http://jeil.jje.hs.kr/jeil-h/food/2020/7/23/lunch"
ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}
req_html = requests.get(url, headers=header)
html = req_html.text

soup = BeautifulSoup(html,'html.parser')
try:
  img_ = 'http://jeil.jje.hs.kr/'+ soup.find('img').get('src')

  urllib.request.urlretrieve(img_,'img.png')

  
except AttributeError:
  imgg = ''
  er = 1

for i in soup.find_all('dd'):
  # print(i.get_text())
  data.append(i.get_text())

for i in data[1]:
  try:
    int(i)
  except ValueError:
    if i != '/' :
      text += i 
  
text = text.split('.')

for i in range(len(text)):
  if text[i] != '' :
    if ')' in text[i]:
      text_data += text[i][:text[i].index(")")+1] + '\n'
    else:
      text_data += text[i] + '\n'
  else:
    text_data += '' 

if '%' in text_data:
  print('1')
  text_data = text_data.replace('%','')


win=tkinter.Tk()
win.title("급식")
win.geometry("640x740+100+100")
win.resizable(False, False)

# req_btn = tkinter.Button(win, text="급식", overrelief="solid", command=req, repeatdelay=1000, repeatinterval=100)
# req_btn.pack()

font = tkinter.font.Font(family="맑은 고딕" ,size=16)

res_label = tkinter.Label(win ,text=text_data ,font=font)
res_label.pack()


if er == 0:
  img = cv2.imread('img.png')
  cv2.imwrite('img.png',img)

  imgg = tkinter.PhotoImage(file='img.png')

img_label = tkinter.Label(win, image = imgg)
if er == 1:
  img_label.config(text='음식사진 업로드 안됨 \n 3교시이후 업로드 예정', font=font)
img_label.pack()

win.mainloop()
if er == 0:
  os.remove('img.png')

