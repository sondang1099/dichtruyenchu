import webbrowser
import keyboard
import time
import pickle

with open('variable.pkl', 'rb') as file:
    url = pickle.load(file)

# pth = "C:\Program Files\Google\Chrome\Application\chrome.exe"
# webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(pth))
# chrome = webbrowser.get('chrome')
# chrome.open_new_tab(url)
webbrowser.open_new_tab(url)
time.sleep(6)
keyboard.press_and_release('ctrl + s')
time.sleep(3)
keyboard.press_and_release('alt + s')
time.sleep(1)