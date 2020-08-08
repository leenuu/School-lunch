from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font
from PIL import Image
import datetime as dy
import requests
import tkinter
import tkinter.ttk
import tkinter.font
import urllib.request
import cv2
import os 

def get_time():
    try:
        print(val.get())
        data = load_workbook(f"시간표 {sh_name}.xlsx", data_only=True)
        ws = data.active

        time = ''

        for p in range(1,14):
            if val.get() == f'{p}반':
                for q in range(3,10):
                    if 15 <= len(str(ws.cell(row=q, column=p+2).value)):
                        time += f'{q-2}교시:' + str(ws.cell(row=q, column=p+2).value) + '\n'
                    else:
                        time += f'{q-2}교시:' + str(ws.cell(row=q, column=p+2).value).replace('\n',' ') + '\n'

        #   for q in range(3,10):
        #         time += f'{q-2}교시:' + str(ws.cell(row=q, column=15).value).replace('\n',' ') + '\n'

        time_label.config(text=time, font=font)

    except NameError:
        time_label.config(text="시간표 업로드 안됨", font=font)

#################################################### food ######################################################################################

data = list()
text_data = '\n'
text = ''
text_ = ''
te = ''
er = 0
url = f'http://jeil.jje.hs.kr/jeil-h/food/2020/{dy.datetime.today().month}/{dy.datetime.today().day}/lunch'
# url = "http://jeil.jje.hs.kr/jeil-h/food/2020/7/28/lunch"

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

# print(te)
for i in te:
  try:
    int(i)
  except ValueError:
    if i != '/' :
      text += i 
  
text = text.split('\n')
# print(text)

for i in range(len(text)):
  if text[i] != '' :
    if ')' in text[i]:
      text_data += text[i][:text[i].index(")")+1] + '\n'
    else:
      text_data += text[i] + '\n'
  else:
    text_data += + '\n' 

if '%' in text_data:
#   print('1')
  text_data = text_data.replace('%','')

if '.' in text_data:
#   print('2')
  text_data = text_data.replace('.','')


#################################################### time_table ######################################################################################

sd_data = ''
get_sd_url = f'http://jeil.jje.hs.kr/jeil-h/0208/board/16996/'

try:
    ua = UserAgent()
    header = {'User-Agent':str(ua.chrome)}
    req_html = requests.get(get_sd_url, headers=header)
    html = req_html.text

    soup = BeautifulSoup(html,'html.parser')

    for i in soup.find('tbody').find_all('a'):
        if f'{dy.datetime.today().month}/{dy.datetime.today().day}' in str(i): 
        # if f'{8}/{31}' in str(i): 
            sd_data = i

    data_url = str(sd_data.get('onclick'))[str(sd_data.get('onclick')).index('(')+1:str(sd_data.get('onclick')).index(')')].split(',')[1].replace("'",'')


    url_sd = f'http://jeil.jje.hs.kr/jeil-h/0208/board/16996/{data_url}'
    print(url_sd)


    req_html = requests.get(url_sd, headers=header)
    html = req_html.text

    soup = BeautifulSoup(html,'html.parser')
    pr = soup.find('dd').find_all('a')[1].get('href')

    sh_name_day = soup.find('dd').find_all('a')[0].get_text()[soup.find('dd').find_all('a')[0].get_text().index("(") : soup.find('dd').find_all('a')[0].get_text().index(")")+1]
    sh_name = f'{dy.datetime.today().month}.{dy.datetime.today().day}{sh_name_day}'
    # sh_name = '날짜'
    # print(sh_name)

    preview_url = f'http://jeil.jje.hs.kr{pr}'

    urllib.request.urlretrieve(preview_url, 'sd.xlsx')

    data = load_workbook("sd.xlsx", data_only=True)
    ds = data.active

    wb = Workbook()
    ws = wb.active

    sum_cell = list()


    for i in range(1,3):
        for j in range(3,11):
            sst = ''
            ws.cell(row=j-1, column=i).value = ds.cell(row=j, column=i).value 
            ws.cell(row=j-1, column=i).font = Font(name='맑은 고딕', size=16, bold=True)
            ws.cell(row=j-1, column=i).alignment = Alignment(horizontal='center', vertical='center',wrapText=True)
            ws.column_dimensions['B'].width = 20

    for i in range(15,28):
        for j in range(3,11):
            if j != 10:
                ws.row_dimensions[j].height = 74
            ws.cell(row=j-1, column=i-12).value = str(ds.cell(row=j, column=i).value)[0:2] + str(ds.cell(row=j, column=i).value)[2:]
            ws.cell(row=j-1, column=i-12).alignment = Alignment(horizontal='center', vertical='center',wrapText=True)
            ws.cell(row=j-1, column=i-12).font = Font(name='맑은 고딕', size=14, bold=True)
            if ds.cell(row=j, column=i).value == None:
                sum_cell.append([i-12, j])

    # print(sum_cell)

    if sum_cell != []:
        for i in range(sum_cell[0][1]-1, sum_cell[len(sum_cell)-1][1]):
            for j in range(sum_cell[0][0], sum_cell[len(sum_cell)-1][0]+1):
                ws.cell(row=i, column=j).value = ws.cell(row=sum_cell[0][1]-1, column=sum_cell[0][0]-1).value
        
    #   ws.merge_cells(start_row= sum_cell[0][1]-1, start_column=sum_cell[0][0]-1,end_row= sum_cell[len(sum_cell)-1][1]-1,end_column=sum_cell[len(sum_cell)-1][0])
    wb.save(f"시간표 {sh_name}.xlsx")

except AttributeError:
    print("시간표 업데이트 안됨")

#################################################### gui ######################################################################################

win=tkinter.Tk()
win.title("급식")
win.geometry("1080x360+100+100")
win.resizable(False, False)

# req_btn = tkinter.Button(win, text="급식", overrelief="solid", command=req, repeatdelay=1000, repeatinterval=100)
# req_btn.pack()


frame1=tkinter.Frame(win, relief="solid", bd=2, width=360, height=480)
frame1.pack(side="right", fill="both", expand=True)

frame2=tkinter.Frame(win, relief="solid", bd=2, width=360, height=480)
frame2.pack(side="right", fill="both", expand=True)

frame3=tkinter.Frame(win, relief="solid", bd=2, width=360, height=480)
frame3.pack(side="right", fill="both", expand=True)

font = tkinter.font.Font(family="맑은 고딕" ,size=14)

sd_label = tkinter.Label(frame3, text='시간표 조회', font=font)
sd_label.pack()

values=[str(i)+"반" for i in range(1, 14)] 

val = tkinter.StringVar()

combobox=tkinter.ttk.Combobox(frame3, textvariable=val, height=15, values=values)
combobox.pack()

combobox.set("반 선택")

sd_brt = tkinter.Button(frame3, text="조회", command=get_time)
sd_brt.pack()

time_label = tkinter.Label(frame3, text='')
time_label.pack()

date_label = tkinter.Label(frame2, text=f'{dy.datetime.today().month}월 {dy.datetime.today().day}일 점심 식단', font=font)
# date_label = tkinter.Label(frame2, text=f'{7}월 {31}일 점심 식단', font=font)
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
if er == 0:
  os.remove('img.png')
os.remove('sd.xlsx')
os.remove(f"시간표 {sh_name}.xlsx")
