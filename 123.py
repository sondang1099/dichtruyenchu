import os

start = int (input("Chap start: "))
end = int (input("Chap end: "))
for i in  range(start, end+1):
    filename = f'D:\\Code\\Python\\dichtruyenchu\\đã dịch\\{i}\\{i}.txt'
    if not os.path.isfile(filename):
        dir_path, file_name = os.path.split(filename)
        filename = os.path.join(dir_path + '_có_ảnh', file_name)
    filename = open(filename, "r", encoding="utf-8")
    content = filename.read()
    f = open("TONG"+f"{start}"+"_"+f"{end}"+".txt", "a", encoding='utf-8')
    f.write(f"CHAP {i}"+"\n"+ content+ "\n\n")