import sys
sys.path.append('./')
from loader import color
from loader import conf
from loader import ultis
from database import connection
import random
from AI import train
# date time
import datetime
import time
# menu 
menu = {
    "rand": "Thêm ngẫu nhiên proxy vào cho những tài khoản chưa có proxy",
    "fill": "Thêm proxy cho những tài khoản chưa có proxy",
    "sec": "Thay proxy cho tài khoản bất kì",
}

# check connection
db = connection.getCol()
if db != None:
    print(color.green, 'Kết nối database thành công', color.end)
else:
    print(color.red, 'Kết nối database thất bại', color.end)
    sys.exit()


ultis.clear()

print(color.yellow, '==>', color.ubgreen, 'Menu', color.end)
for KEY, VALUE in menu.items():
    print(color.yellow, '[' + color.cyan + KEY + color.yellow + ']', color.white, '=', color.purple, VALUE)
choice = input(color.yellow + 'Chọn chức năng: ' + color.end)


# input
proxyFile = input(color.yellow + 'Nhập đường dẫn file proxy: ' + color.end)
if ultis.checkFileExsit(proxyFile) == False:
    print(color.red, 'File proxy không tồn tại', color.end)
    sys.exit()
defaultFormat = [
    'ip',
    'port',
    'user',
    'pasw',
]

format = input(color.yellow + 'Nhập định dạng proxy (' + ', '.join(defaultFormat) + '): ' + color.end)
format = format.split(',')
format = [x.strip() for x in format if x.strip() in defaultFormat]
splitCharacter = input(color.yellow + 'Nhập ký tự phân tách proxy: ' + color.end)
# read file proxy
with open(proxyFile, 'r') as f:
    proxies = f.readlines()
proxies = [x.strip() for x in proxies]

proxys = []
if "user" in format and "pasw" in format:
    for proxy in proxies:
        if proxy == '': continue
        ip = ''
        port = ''
        user = ''
        pasw = ''
        proxy = proxy.split(splitCharacter)
        for name in defaultFormat:
            try:
                index = format.index(name)
                if name == 'port':
                    port = proxy[index]
                elif name == 'user':
                    user = proxy[index]
                elif name == 'pasw':
                    pasw = proxy[index]
                else:
                    ip = proxy[index]
                
            except:
                pass

        proxys.append(
                f'{user}:{pasw}@{ip}:{port}'
            )
            
else:
    for proxy in proxies:
        if proxy == '': continue
        ip = ''
        port = ''
        proxy = proxy.split(splitCharacter)
        for name in defaultFormat:
            try:
                index = format.index(name)
                if name == 'port':
                    port = proxy[index]
                else:
                    ip = proxy[index]
            except:
                pass
        proxys.append(
            f'{ip}:{port}'
        )
        
if choice == "rand":
    print(color.yellow, '==>', color.ubgreen, 'Số lượng proxy quét được trong file theo format: ', color.end, len(proxys))
    print(color.yellow, '==>', color.ubgreen, 'Số lượng tài khoản chưa có proxy: ', color.end, connection.getCountAccountFBNoProxy())


    for acc in connection.getAccountFBNoProxy():
        randProxy = random.choice(proxys)
        connection.updateProxyAccountFB(acc['uid'], randProxy)
    print(color.yellow, '==>', color.green, 'Thêm proxy thành công', color.end)
    print(color.yellow, '==>', color.ubgreen, 'Số lượng tài khoản chưa có proxy sau khi thêm: ', color.end, connection.getCountAccountFBNoProxy())

elif choice == 'fill':
    print(color.yellow, '==>', color.ubgreen, 'Số lượng proxy quét được trong file theo format: ', color.end, len(proxys))
    print(color.yellow, '==>', color.ubgreen, 'Số lượng tài khoản chưa có proxy: ', color.end, connection.getCountAccountFBNoProxy())
    accountsFB = connection.getAccountFBNoProxy()
    for index in range(len(proxys)):
        if index >= len(accountsFB): break
        connection.updateProxyAccountFB(accountsFB[index]['uid'], proxys[index])
        print(color.yellow, '==>', color.green, 'Thêm proxy thành công cho tài khoản: ', color.end, accountsFB[index]['uid'])
elif choice == 'sec':
    print(color.yellow, '==>', color.ubgreen, 'Số lượng proxy quét được trong file theo format: ', color.end, len(proxys))
   
    accountsFB = connection.getAllAccountFB()
    print(color.yellow, '==>', color.ubgreen, 'Số lượng tài khoản đã có proxy hoặc không: ', color.end, len(accountsFB))
    for acc in accountsFB:
        print(color.yellow, '==>', color.ubgreen, 'Thay proxy cho tài khoản: ', color.end, acc['uid'])
    uid = input(color.yellow + 'Nhập uid tài khoản cần thay proxy: ' + color.end)


    # print list proxy
    print(color.yellow, '==>', color.ubgreen, 'Danh sách proxy: ', color.end)
    for index in range(len(proxys)):
        print(color.yellow, '[' + color.cyan + str(index) + color.yellow + ']', color.white, '=', color.purple, proxys[index])
    proxyIndex = input(color.yellow + 'Chọn vị trí proxy muốn tham vào: ' + color.end)
    try:
        proxyIndex = int(proxyIndex)
        if proxyIndex >= len(proxys):
            print(color.red, 'Vị trí proxy không hợp lệ', color.end)
            sys.exit()

        connection.updateProxyAccountFB(uid, proxys[proxyIndex])
        print(color.yellow, '==>', color.green, 'Thay proxy thành công cho tài khoản: ', color.end, uid)
    except:
        print(color.red, 'Vị trí proxy không hợp lệ', color.end)
        sys.exit()    
    