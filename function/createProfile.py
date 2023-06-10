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
# threading
import threading

# create
from chrome import loginFacebookGetProfile
# check connection
db = connection.getCol()
if db != None:
    print(color.green, 'Kết nối database thành công', color.end)
else:
    print(color.red, 'Kết nối database thất bại', color.end)
    sys.exit()


ultis.clear()
# menu 
menu = {
    'one': 'Tạo profile cho một uid',
    'all': 'Tạo hàng loạt cho uid chưa có profile'
}
config = conf.config
# get all account
accounts = connection.getAllAccountFB()
ids = []
noProfileids = []
for acc in accounts:
    if 'profile_path' not in acc:
        if 'proxy' not in acc:
            acc['proxy'] = ''
        print(color.red, 'Chưa có profile cho uid: ', color.end, color.yellow, acc['uid'] +' | proxy ' + acc["proxy"], color.end)
        noProfileids.append(acc['uid'])
    else:
        print(color.green, 'Đã có profile cho uid: ', color.end, color.yellow, acc['uid'], color.end)
    ids.append(acc['uid'])
        
        


# out menu
print(color.yellow, '==>', color.ubgreen, 'Menu', color.end)
for KEY, VALUE in menu.items():
    print(color.yellow, '[' + color.cyan + KEY + color.yellow + ']', color.white, '=', color.purple, VALUE)
choice = input(color.yellow + 'Chọn chức năng: ' + color.end)


if choice == 'one':
    id = input(color.yellow + 'Nhập uid: ' + color.end)
    if id in ids:
        session = loginFacebookGetProfile.newSession(id, '', connection)
        session.start()

    else:
        print(color.red, 'Không tồn tại uid', color.end)
        sys.exit()
elif choice == 'all':
    limit_thread_per_time = int(config.get('run', 'thread_max'))

    threads = []
    startCreate = lambda id: loginFacebookGetProfile.newSession(id, '', connection).start()
    num_threads = len(noProfileids)

    for i in range(num_threads):
        thread = threading.Thread(target=startCreate, args=(noProfileids[i],))
        threads.append(thread)
        thread.start()
        if (i + 1) % limit_thread_per_time == 0 or i == num_threads - 1:
            for t in threads:
                t.join()
            threads = []