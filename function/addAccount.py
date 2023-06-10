
import sys
sys.path.append('./')
from loader import color
from loader import conf
from loader import ultis
from database import connection
from AI import train
# date time
import datetime
import time
# menu 
menu = {
    "txt": "Thêm tài khoản bằng import file"
}

# check connection
db = connection.getCol()
if db != None:
    print(color.green, 'Kết nối database thành công', color.end)
else:
    print(color.red, 'Kết nối database thất bại', color.end)
    sys.exit()


ultis.clear()


# out count account fb
count = connection.getCountAccountFB()
print(color.green, 'Số lượng account fb hiện tại: ', color.end, color.yellow, count, color.end)


# out menu
print(color.yellow, '==>', color.ubgreen, 'Menu', color.end)
for KEY, VALUE in menu.items():
    print(color.yellow, '[' + color.cyan + KEY + color.yellow + ']', color.white, '=', color.purple, VALUE)


#choice = input(color.yellow + 'Chọn chức năng: ' + color.end)

choice = "txt"

if choice == "txt":
    file = input(color.yellow + 'Nhập đường dẫn chứa tài khoản: ' + color.end)
    strAcc = []
    # check exsit
    if ultis.checkFileExsit(file) == False:
        print(color.red, 'File không tồn tại', color.end)
        sys.exit()
    
    # read file
    with open(file, 'r', encoding='utf-8') as f:
        strAcc = f.read().split("\n")

    keys_list = [
        'uid',
        'password',
        '2fa',
        'cookie',
        'token',
        'email',
        'pass_email',
        'birthday',
        'proxy'
    ]

    # convert to string
    keys = ', '.join(keys_list)
    format = input(color.yellow + 'Nhập định dạng tài khoản (' + keys + '): ' + color.end)
    splitCharacter = input(color.yellow + 'Nhập kí tự phân tách: ' + color.end)

    format = format.split(',')
    format = [x.strip() for x in format if x.strip() in keys_list]
    print('Định dạng tài khoản dã kiểm tra tồn tại: ', color.green, format)

    for acc in strAcc:
  
        if acc == '':
            pass
        acc = acc.split(splitCharacter)
        if len(acc) == len(format):
   
            account = {}
            account['format'] = format
            for name in format:
                account[name] = acc[format.index(name)]
            try:
                print(account)
                count = connection.insertAccountFB(account)
                print(color.green, 'Thêm thành công tài khoản', color.end, color.yellow, count, color.end)
            except Exception as e:
                print(color.red, 'Thêm thất bại tài khoản', color.end, color.yellow, e, color.end)




