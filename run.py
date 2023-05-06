import os
import re
import pickle
import pyautogui
import time

url = input("Nhập URL: ")
end = input("Chap kết thúc: ")
#match = re.search(r'(\d+)/$', url)
count = 0
new_number = 0
while end != new_number:
    if count == 0:
        with open("variable.pkl", "wb") as f:
            pickle.dump((url), f)
        match = re.search(r'(\d+)/$', url)
        new_number = str(int(match.group(1)))
        #exec(open("dich.py").read())
        exec(open("import requests.py").read())
        count += 1
        os.remove("variable.pkl")
    else:
        match = re.search(r'(\d+)/$', url)
        if match:
            new_number = str(int(match.group(1)) + 1)
            url = re.sub(r'\d+/$', new_number + '/', url)
            with open("variable.pkl", "wb") as f:
                pickle.dump((url), f)
            #exec(open("dich.py").read())
            exec(open("import requests.py").read())
            count += 1
            if count == 10:
                time.sleep(40)
                for i in range(10):
                    pyautogui.hotkey('ctrl', 'w')
                count = 0
            os.remove("variable.pkl")
        