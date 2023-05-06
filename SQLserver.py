import pyodbc
import pandas as pd


cnxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=SONDANG\\SONDANG1099;DATABASE=sondang;UID=sa;PWD=sondang1099")

# Tạo đối tượng cursor để thực thi các câu lệnh SQL
cursor = cnxn.cursor()

# # Thực thi stored procedure và lấy dữ liệu
# cursor.execute("Get_All_Tu_loi")

# # Lấy kết quả trả về
# words = cursor.fetchall()
# file_path = "D:\\Code\\Python\\dichtruyenchu\\đã dịch\\700\\700.txt"
# with open(file_path, "r", encoding="utf-8") as f:
#     content = f.read()
# # df = pd.DataFrame({"sentence": content.split(".")})
# df = content.split("\n")
# for row in df:
#     cursor.execute("INSERT INTO dbo.Content ( Cau ) VALUES (?)", (row))
# filename = '72b114dfc450a97f6176f478e5bbace5x50.jpg'
# cursor.execute("SELECT Image FROM dbo.Image_QC")
# unwanted_urls = cursor.fetchall()

# print(type(unwanted_urls))
# unwanted_urls1 = ['avatar92.jpg','72b114dfc450a97f6176f478e5bbace5x50.jpg','72b114dfc450a97f6176f478e5bbace5x80.jpg','icon.png',
#                             'foxaholic-logo-with-red-stripe.png','300x250-1.png','728x90-1(1).png','728x90-1.png','300x250-2.png','300x250-3.png',
#                             'kofi3.png','dfc2b46416444282bbfc08c49120750a_970x250.png','en.png']
# print(type(unwanted_urls1))
# for unwanted_url in unwanted_urls:
#     if filename == unwanted_url[0]:
#         break
# else:
#     a=1
line_trans = "[……asdwdsad-san.]"
cursor.execute("Get_All_Tu_loi")
words = cursor.fetchall()
line_new = ""
for word in words:
    if word[0] in line_trans:
        cursor.execute('EXEC Get_tu_thay_the_by_Tu_loi @Tu_loi = ?', (word[0],))
        word_replace = cursor.fetchall()
        line_new = line_trans.replace(word[0], word_replace[0][0])
else:
    if line_new == "":
        line_new = line_trans
# Lưu thay đổi
cnxn.commit()

# Đóng kết nối
cnxn.close()    