from gtts import gTTS
import subprocess

with open("D:\Code\Python\dichtruyenchu\TONG577_700.txt", "r", encoding="UTF-8") as f:
    text = f.read()
sentences = text.split('\n')    
i=0
def convermp3(s):
    # try:
    # # đoạn mã có thể gây ra lỗi
    #     tts = gTTS(s, lang='vi')
    #     tts.save("Tong.mp3")
    #     i += 1
    #     print(i)
    # except:
    # # xử lý lỗi và tiếp tục chạy chương trình
    #     return
    tts = gTTS(s, lang='vi')
    tts.save("Tong.mp3")
def text_to_speech(text, output_file):
    # chạy lệnh PicoTTS để chuyển đổi văn bản sang giọng nói
    subprocess.call(['pico2wave', '-l', 'vi-VN', '-w', output_file, text])    
for x in sentences:
  convermp3(str(x))
