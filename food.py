from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import datetime as dy
import requests
import tkinter
import tkinter.ttk
import tkinter.font
import urllib.request
import cv2
from PIL import Image
import os 

def get_sd():
  
  sd_data = ''
  get_sd_url = f'http://jeil.jje.hs.kr/jeil-h/0208/board/16996/'

  ua = UserAgent()
  header = {'User-Agent':str(ua.chrome)}
  req_html = requests.get(get_sd_url, headers=header)
  html = req_html.text

  soup = BeautifulSoup(html,'html.parser')

  for i in soup.find('tbody').find_all('a'):
      if f'{dy.datetime.today().month}/{dy.datetime.today().day}' in str(i):
          sd_data = i

  data_url = str(sd_data.get('onclick'))[str(sd_data.get('onclick')).index('(')+1:str(sd_data.get('onclick')).index(')')].split(',')[1].replace("'",'')


  url_sd = f'http://jeil.jje.hs.kr/jeil-h/0208/board/16996/{data_url}'
  print(url_sd)


data = list()
text_data = '\n'
text = ''
text_ = ''
te = ''
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

  image = Image.open('img.png')

  resize_image = image.resize((360,360))

  resize_image.save('img.png')
  
except AttributeError:
  imgg = ''
  er = 1

te = str(soup.find_all('dd')[1]).replace('<br/>','\n').replace('<dd>','').replace('</dd>','')

for i in te:
  try:
    int(i)
  except ValueError:
    if i != '/' :
      text += i 
  
text = text.split('.')

for i in range(len(text)):
  if text[i] != '' :
    if ')' in text[i]:
      text_data += text[i][:text[i].index(")")+1] 
    else:
      text_data += text[i] 
  else:
    text_data += '' 

if '%' in text_data:
  print('1')
  text_data = text_data.replace('%','') + '\n'


win=tkinter.Tk()
win.title("급식")
win.geometry("1080x360+100+100")
win.resizable(False, False)

# req_btn = tkinter.Button(win, text="급식", overrelief="solid", command=req, repeatdelay=1000, repeatinterval=100)
# req_btn.pack()


frame1=tkinter.Frame(win, relief="solid", bd=2)
frame1.pack(side="right", fill="both", expand=True)

frame2=tkinter.Frame(win, relief="solid", bd=2)
frame2.pack(side="right", fill="both", expand=True)

frame3=tkinter.Frame(win, relief="solid", bd=2)
frame3.pack(side="right", fill="both", expand=True)

font = tkinter.font.Font(family="맑은 고딕" ,size=14)

sd_label = tkinter.Label(frame3, text='시간표 조회', font=font)
sd_label.pack()

values=[str(i)+"반" for i in range(1, 14)] 

combobox=tkinter.ttk.Combobox(frame3, height=15, values=values)
combobox.pack()

combobox.set("반 선택")

sd_brt = tkinter.Button(frame3, text="조회", command=get_sd)
sd_brt.pack()

date_label = tkinter.Label(frame2, text=f'{dy.datetime.today().month}월 {dy.datetime.today().day}일 점심 식단', font=font)
date_label.pack()

res_label = tkinter.Label(frame2 ,text=text_data ,font=font)
res_label.pack()


if er == 0:
  img = cv2.imread('img.png')
  cv2.imwrite('img.png',img)

  imgg = tkinter.PhotoImage(file='img.png')

img_label = tkinter.Label(frame1, image = imgg)
if er == 1:
  img_label.config(text='\n\n음식사진 업로드 안됨 \n 3교시이후 업로드 예정', font=font)
img_label.pack()

win.mainloop()
# if er == 0:
#   os.remove('img.png')

