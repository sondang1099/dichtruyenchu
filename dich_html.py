from io import open
from bs4 import BeautifulSoup
import time
import requests
import json
import os
import sys
import shutil
import pyodbc

def translate(text):
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
def write(filename, line_new):
    f = open(filename, "a", encoding='utf-8')
    f.write(line_new+ "\n")
    return
def html_to_text(name_html):
    with open(name_html, 'r', encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        count = -2
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
    
data = input()
# Thực thi stored procedure và lấy dữ liệu
cnxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=SONDANG\SONDANG1099;DATABASE=sondang;UID=sa;PWD=sondang1099")
cursor = cnxn.cursor()
cursor.execute("Get_All_Tu_loi")
words = cursor.fetchall()
#
script_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(script_dir, 'html', data)
file_number = data.split(" ")[0]
if folder_path.endswith('.html'):
    html_to_text(folder_path)                     
    if os.path.exists(f"D:\Code\Python\dichtruyenchu\đã dịch\{file_number}"):
        shutil.rmtree(f"D:\Code\Python\dichtruyenchu\đã dịch\{file_number}")
    os.mkdir(f"D:\Code\Python\dichtruyenchu\đã dịch\{file_number}")
    file_name = f"D:\Code\Python\dichtruyenchu\đã dịch\{file_number}\{file_number}.txt"
    countxt = 0
    with open('web.txt', encoding="utf-8") as file:
        file_content = []
        line_old = ''
        if os.path.exists(file_name):
            os.remove(file_name)
        for line in file:
            line = line.rstrip('\n')
            line = line.replace('\xa0', ' ')
            line = line.lstrip()
            file_content.append(line)
            if line_old == line:
                continue
            if line == '\n':
                f = write(file_name, line)
                continue
            if line == '':
                continue
            if 'Alice’s mouth were a bit dirty' in line :
                a = 1
            line_trans = translate(line)
            line_new = ""
            for word in words:
                if word[0] in line_trans:
                    cursor.execute('EXEC Get_tu_thay_the_by_Tu_loi @Tu_loi = ?', (word[0],))
                    word_replace = cursor.fetchall()
                    line_new = line_trans.replace(word[0], word_replace[0][0])
            else:
                if line_new == "":
                    line_new = line_trans
            f = write(file_name, line_new)
            line_old = line
            countxt += 1
            if countxt == 69:
                c =2
    print(f'Hoàn thành dịch chap {file_number}!')        
    os.remove('web.txt')                        
else:
    for filename in os.listdir(folder_path):
        if os.path.splitext(filename)[1].lower() in ('.jpg', '.png'):
            cursor.execute("SELECT Image FROM dbo.Image_QC")
            unwanted_urls = cursor.fetchall()
            for unwanted_url in unwanted_urls:
                if filename == unwanted_url[0]:
                    break
            else:
                old_folder_name = f"D:\\Code\\Python\\dichtruyenchu\\đã dịch\\{file_number}"
                new_folder_name = f"D:\\Code\\Python\\dichtruyenchu\\đã dịch\\{file_number}_có_ảnh"
                if os.path.exists(old_folder_name):
                    shutil.copytree(old_folder_name, new_folder_name)
                    shutil.rmtree(old_folder_name)
                shutil.move(os.path.join(folder_path, filename), os.path.join(new_folder_name, filename))
                print(f'Hoàn lấy ảnh chap {file_number}!')                    
sys.stdout.flush()