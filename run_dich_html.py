import os
import subprocess
import re
import pickle
import pyautogui
import time
import shutil

url = input("Nhập URL: ")
start = 0
end = input("Chap kết thúc: ")
if os.path.exists(f"D:\Code\Python\dichtruyenchu\HTML"):
    pass
else:
    os.mkdir(f"D:\Code\Python\dichtruyenchu\HTML")
count = -1
new_number = 0
while end != new_number:
    if count == -1:
        with open("variable.pkl", "wb") as f:
            pickle.dump((url), f)
        match = re.search(r'(\d+)/$', url)
        new_number = str(int(match.group(1)))
        start = new_number
        exec(open("lay_html.py").read())
        count += 1
        os.remove("variable.pkl")
    else:
        match = re.search(r'(\d+)/$', url)
        new_number = str(int(match.group(1)) + 1)
        url = re.sub(r'\d+/$', new_number + '/', url)
        with open("variable.pkl", "wb") as f:
            pickle.dump((url), f)
        exec(open("lay_html.py").read())
        count += 1
        if count == 10:
            time.sleep(40)
            for i in range(10):
                pyautogui.hotkey('ctrl', 'w')
            count = 0
        os.remove("variable.pkl")
time.sleep(40)
for i in range(count+1):
    pyautogui.hotkey('ctrl', 'w')
folder_path = "D:\Code\Python\dichtruyenchu\HTML"
directories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
numbers = [int(re.findall(r'\d+', folder)[0]) for folder in directories]
full_number_list = [i for i in range(min(numbers), max(numbers)+1)]
missing_numbers = set(full_number_list) - set(numbers)
if missing_numbers:
    for x in  missing_numbers:
        url = re.sub(r'\d+/$', str(x) + '/', url)
        with open("variable.pkl", "wb") as f:
            pickle.dump((url), f)
        exec(open("lay_html.py").read())
        os.remove("variable.pkl")

# Lấy danh sách tất cả các đối tượng trong thư mục
all_objects = os.listdir(folder_path)

for folder_name in all_objects:
    print(f'Bắt đầu xử lý {folder_name}!')
    receiver = subprocess.Popen(["python", "dich_html.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    receiver.stdin.write(folder_name.encode())
    receiver.stdin.close()
    print(receiver.communicate()[0].decode())
shutil.rmtree(f"D:\Code\Python\dichtruyenchu\HTML")