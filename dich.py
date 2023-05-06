import os
import re
import requests
import time
import shutil
import json
from bs4 import BeautifulSoup
import pickle

if os.path.exists('wed.txt'):
    os.remove('wed.txt')
with open('variable.pkl', 'rb') as file:
    url = pickle.load(file)    
response = requests.get(url)
content = response.content
count = -2
soup = BeautifulSoup(response.content, "html.parser")
images = soup.find_all('img') 
for tag in soup.find_all():
    if tag.name == 'p':
        if count == -2:
            count += 1
            continue
        elif count == -1:
            count = 0
        f = open('web.txt', "a", encoding='utf-8')
        f.write(tag.text + "\n")
        count = 0    
    else:
        if count >= 0:
            count += 1
            if count == 10:
                break
result = re.findall(r'^https?://[^/]+/[^/]+/[^/]+/([^/]+)/$', url)
page_number = result[0]
if os.path.exists(f"D:\Code\Python\dichtruyenchu\đã dịch\{page_number}"):
    shutil.rmtree(f"D:\Code\Python\dichtruyenchu\đã dịch\{page_number}")
os.mkdir(f"D:\Code\Python\dichtruyenchu\đã dịch\{page_number}")
folder_path = f"D:\Code\Python\dichtruyenchu\đã dịch\{page_number}"
filename = f"{folder_path}\{page_number}.txt"
print(f'Bắt đầu dịch chap {page_number}!')
i = 0
exist = 0
for image in images:
    img_url = image['src']
    unwanted_urls = ['https://www.foxaholic.com/wp-content/uploads/2019/12/foxaholic-logo-with-red-stripe.png',
                 'https://az743702.vo.msecnd.net/cdn/kofi3.png?v=2',
                 'https://www.paypal.com/en_US/i/scr/pixel.gif',
                 '/favicon.ico']
    if img_url in unwanted_urls:
        continue
    else:
        if os.path.exists(f"D:\Code\Python\dichtruyenchu\đã dịch\{page_number}"):
            shutil.rmtree(f"D:\Code\Python\dichtruyenchu\đã dịch\{page_number}")
        if exist == 0:
            if os.path.exists(f"D:\Code\Python\dichtruyenchu\đã dịch\{page_number}_có_ảnh"):
                shutil.rmtree(f"D:\Code\Python\dichtruyenchu\đã dịch\{page_number}_có_ảnh")
            os.mkdir(f"D:\Code\Python\dichtruyenchu\đã dịch\{page_number}_có_ảnh")
            exist = 1
        folder_path = f"D:\Code\Python\dichtruyenchu\đã dịch\{page_number}_có_ảnh"
        filename = f"{folder_path}\{page_number}.txt"
        if i == 0:
            x = 0
            r = requests.get(img_url, stream=True)
            while r.status_code != 200:
                x+=1
                print(f"download lỗi image thử lại sau 5s lần thứ {x}")
                r = requests.get(img_url, stream=True)
                time.sleep(5)
            print('download image')
            if ".png" in img_url:
                with open(f"{folder_path}\{page_number}.png", 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    i=1
            elif ".jpg" in img_url:
                with open(f"{folder_path}\{page_number}.jpg", 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    i=1        
        else:
            r = requests.get(img_url, stream=True)            
            while r.status_code != 200:
                x+=1
                print(f"download lỗi image thử lại sau 5s lần thứ {x}")
                r = requests.get(img_url, stream=True)
                time.sleep(5)
            print('download image')
            if ".png" in img_url:
                with open(f"{folder_path}\{page_number}_{i}.png", 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    i+=1
            elif ".jpg" in img_url:
                with open(f"{folder_path}\{page_number}_{i}.jpg", 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    i+=1  
def translate_text(text):
    max_retries = 10
    retries = 0
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={0}&tl={1}&dt=t&q={2}"
    sl = "en"
    tl = "vi"
    formatted_url = url.format(sl, tl, requests.utils.quote(text))
    while retries < max_retries:
        try:
            response = requests.get(formatted_url)
            if response.status_code == 200:
                response_json = json.loads(response.text)
                line_new = " ".join([x[0] for x in response_json[0]])
                return line_new
            else:
                raise Exception("Không thể kết nối đến translate.googleapis.com")
        except Exception as e:
            retries += 1
            if retries == max_retries:
                raise e
            print(f"Kết nối thất bại, chờ 5 giây rồi thử lại ({retries}/{max_retries})")
            time.sleep(5)
    response_json = json.loads(response.text)
    line_new = " ".join([x[0] for x in response_json[0]])
    return line_new
def Write(line_new):
    f = open(filename, "a", encoding='utf-8')
    f.write(line_new+ "\n")
    return
countxt = 0    
with open('wed.txt', encoding="utf-8") as file:
    file_content = []
    line_old = ''
    if os.path.exists(filename):
        os.remove(filename)
    for line in file:
        line = line.rstrip('\n')
        line = line.replace('\xa0', ' ')
        line = line.lstrip()
        file_content.append(line)
        if line_old == line:
            continue
        if line == '\n':
            f = Write(line)
            continue
        if line == '':
            continue
        if 'Alice’s mouth were a bit dirty' in line :
            a = 1
        line_new = translate_text(line)
        f = Write(line_new)
        line_old = line
        countxt += 1
        print(f'Số câu đã dịch chap {page_number}: {countxt}')
        if countxt == 69:
            c =2
print(f'Hoàn thành dịch chap {page_number}!')        
os.remove('web.txt')