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
from Traodoisub import login
from Traodoisub import get_job
from Traodoisub import info
from Traodoisub import claim
from chrome import helper
from facebookDriver import action

sys.path.append('./FeedingFB')
from Hand_gestures import Search
from Hand_gestures import Surfing
from Texting import Messenger

# Tiknter import
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
import time
import datetime
import random
db = connection.getCol()
if db != None:
    print(color.green, 'Kết nối database thành công', color.end)
else:
    print(color.red, 'Kết nối database thất bại', color.end)
    sys.exit()


ultis.clear()
userDirector = {}

config = conf.config

# create form
window = Tk()
window.title("Tool traodoisub.com LIKE GIÁ CAO")
window.geometry('1000x500')
countAccountFB = len(connection.getAllAccountFB())
countAccountFBLive = connection.getCountAccountFBLive()
countAccountFBDie = countAccountFB - countAccountFBLive
labelCountAccount = Label(window, text=f'Tổng số tài khoản: {countAccountFB}')
labelCountAccount.pack()
labelCountAccountLive = Label(window, text=f'Tổng số tài khoản sống: {countAccountFBLive}')
labelCountAccountLive.pack()
labelCountAccountDie = Label(window, text=f'Tổng số tài khoản chết: {countAccountFBDie}')
labelCountAccountDie.pack()
# input delay nghỉ lấy job
labelDelay = Label(window, text="Nhập delay nghỉ lấy job (giây): ")
labelDelay.pack()
EntryDelay = Entry(window, width=50)
EntryDelay.pack()
EntryDelay.insert(0, 60)
# input delay giữa các job
labelDelayJob = Label(window, text="Nhập delay giữa các job (giây): ")
labelDelayJob.pack()
EntryDelayJob = Entry(window, width=50)
EntryDelayJob.pack()
EntryDelayJob.insert(0, 60)


# function

def adđAccTDS():
    # mini form
    windowAddAccTDS = Tk()
    windowAddAccTDS.title("Thêm tài khoản TDS")
    windowAddAccTDS.geometry('500x500')
    # label
    labelAcc = Label(windowAddAccTDS, text="Nhập tài khoản tds: ")
    labelAcc.pack()
    # input
    inputAccTDS = Entry(windowAddAccTDS, width=50)
    inputAccTDS.pack()
    
    labelPassword = Label(windowAddAccTDS, text="Nhập mật khẩu tds: ")
    labelPassword.pack()
    # input
    inputPasswordTDS = Entry(windowAddAccTDS, width=50)
    inputPasswordTDS.pack()

    # selector id fb
    getAllAccountFB = connection.getAllAccountFB()
    listIdFB = []
    for acc in getAllAccountFB:
        listIdFB.append(acc['uid'])
    labelIdFB = Label(windowAddAccTDS, text="Chọn id fb: ")
    labelIdFB.pack()
    selectIdFB = ttk.Combobox(windowAddAccTDS, values=listIdFB)
    selectIdFB.pack()

    # proxy get job
    labelProxy = Label(windowAddAccTDS, text="Nhập proxy get job: ")
    labelProxy.pack()
    # input
    inputProxy = Entry(windowAddAccTDS, width=50)
    inputProxy.pack()

    # button add
    btnAdd = Button(windowAddAccTDS, text="Thêm", command=lambda: [
        connection.addAccTDS(inputAccTDS.get(), inputPasswordTDS.get(), selectIdFB.get(), inputProxy.get()),
        messagebox.showinfo("Thông báo", "Thêm thành công"),
        reloadList(),
        windowAddAccTDS.destroy()
        ])
    
    btnAdd.pack()
    # loop
    windowAddAccTDS.mainloop()
fb_feeding = False
def onFeeding ():
    global fb_feeding
    fb_feeding = True
    messagebox.showinfo("Thông báo", "Đã bật feeding")
def offFeeding ():
    global fb_feeding
    fb_feeding = False
    messagebox.showinfo("Thông báo", "Đã tắt feeding")

btnOnFeeding  = Button(window, text="Bật feeding", command=onFeeding)
btnOnFeeding.pack()
btnOffFeeding  = Button(window, text="Tắt feeding", command=offFeeding)
btnOffFeeding.pack()
# button add acc tds
btnAddAccTDS = Button(window, text="Thêm tài khoản TDS", command=adđAccTDS)
btnAddAccTDS.pack()

# listbox
listbox = Listbox(window, width=150, height=150)
listbox.pack()


def reloadList (reload_first=False):
    if reload_first:
        listbox.delete(0, END)
    
        for acctds in connection.getALLAccTDS():
            listbox.insert(END, acctds['user'] + " - " + acctds['pass'] + " - " + acctds['uid'])
            userDirector[acctds['user']] = False
        return True
    listbox.delete(0, END)
    
    for acctds in connection.getALLAccTDS():
        listbox.insert(END, acctds['user'] + " - " + acctds['pass'] + " - " + acctds['uid'])

def checkLogin ():
    currentSelect = listbox.curselection()

    if currentSelect:

        item = listbox.get(currentSelect[0])
        # get uid
        user = item.split(' - ')[0]
        getFullInfo = connection.getTDSAccount(user)
        getFullInfoFB = connection.getAccountFB(getFullInfo['uid'])
        session = login.session(getFullInfo["user"], getFullInfo["pass"], getFullInfoFB['proxy'])
        cookies = session.login()
        if cookies == False:
            # edit text item in listbox
            listbox.delete(currentSelect[0])

            listbox.insert(currentSelect[0], user + " - " + getFullInfo["pass"] + " - " + getFullInfo["uid"] + " - " + "Đăng nhập thất bại")
        else:
            # edit text item in listbox
            listbox.delete(currentSelect[0])
            
            listbox.insert(currentSelect[0], user + " - " + getFullInfo["pass"] + " - " + getFullInfo["uid"] + " - " + "Đăng nhập thành công")

def run():     
    currentSelect = listbox.curselection()
    feedingFunction = ['Search', 'Surfing', 'Messenger']
    if currentSelect:
        currentStt = 0
        item = listbox.get(currentSelect[0])
        # get uid
        user = item.split(' - ')[0]
        getFullInfo = connection.getTDSAccount(user)
        getFullInfoFB = connection.getAccountFB(getFullInfo['uid'])
        getTime = lambda: str(datetime.datetime.now())
        updateMessage = lambda message: [listbox.delete(currentSelect[0]),
                                         listbox.insert(currentSelect[0], getTime() + ' - ' + user + " - " + getFullInfo["pass"] + " - " + getFullInfo["uid"] + " - " + message)]
        updateStatusBarAccount = lambda user, xu, proxy, uid, message:  [listbox.delete(currentSelect[0]),
                                         listbox.insert(currentSelect[0], f'{getTime()} - {user} - {xu} - {proxy} - {uid} - {message} - Job success: {currentStt}')]
        if 'proxy' not in getFullInfoFB:
            # edit text item in listbox
            updateMessage("Không có proxy")
            return False
        
        session = login.session(getFullInfo["user"], getFullInfo["pass"], getFullInfo['proxy'])
        cookies = session.login()
        if cookies == False:
            
            updateMessage("Đăng nhập thất bại")
            listbox.delete(currentSelect[0]),
            listbox.insert(currentSelect[0], user + " - " + getFullInfo["pass"] + " - " + getFullInfo["uid"] + " - Đăng nhập thất bại!")
            return False
        else:
            updateMessage("Đăng nhập thành công")
        updateMessage('Đang đặt nick cấu hình')
        setNick = info.session(cookies, getFullInfo['proxy'])
        if setNick.datnick(getFullInfo["uid"]):
            updateMessage('Đặt nick thành công')
        else:
            updateMessage('Đặt nick thất bại')
            listbox.delete(currentSelect[0]),
            listbox.insert(currentSelect[0], user + " - " + getFullInfo["pass"] + " - " + getFullInfo["uid"] + " - Đăt nick thất bại")
            return False
        userInfo = setNick.getInfo()
        if 'xu' in userInfo:
            updateStatusBarAccount(user, userInfo['xu'], getFullInfoFB['proxy'], getFullInfo["uid"], 'Đang chạy')
        else:
            updateStatusBarAccount(user, '0', getFullInfoFB['proxy'], getFullInfo["uid"], 'Đang chạy')
        headless = False
        if config.get('chrome_setting', 'headless_mode') == '1':
            headless = True
      
        chrome = helper.createDriver(profile_path=getFullInfoFB["profile_path"], 
                                path_driver=config.get('chrome_setting', 'chromedriver_path'),
                                  headless_mode=headless,
                                    proxy=getFullInfoFB["proxy"])
        

        actionFB = action.Action(chrome)
        
        error = 0
        while True:
            
            try:
                if userDirector[user] == True:
                    listbox.delete(currentSelect[0]),
                    listbox.insert(currentSelect[0], user + " - " + getFullInfo["pass"] + " - " + getFullInfo["uid"] + " - Đã ngưng chạy!")
                    return True
                time.sleep(5)
                updateStatusBarAccount(user, userInfo['xu'], getFullInfoFB['proxy'], getFullInfo["uid"], f'Làm mới phiên...')
                session = login.session(getFullInfo["user"], getFullInfo["pass"], getFullInfo['proxy'])
                cookies = session.login()
                setNick = info.session(cookies, getFullInfo['proxy'])
                setNick.datnick(getFullInfo["uid"])
                job = get_job.session(cookies, getFullInfo['proxy'])
                claim_job = claim.session(cookies, getFullInfo['proxy'])
                updateStatusBarAccount(user, userInfo['xu'], getFullInfoFB['proxy'], getFullInfo["uid"], f'Đang lấy job...')
                getJob = job.like_vip()
                
                
                if getJob[0] == False:
                    message = getJob[1]
                    updateMessage(message)
                else:
                    
                    for job in getJob[1]:
                        if userDirector[user] == True:
                            listbox.delete(currentSelect[0]),
                            listbox.insert(currentSelect[0], user + " - " + getFullInfo["pass"] + " - " + getFullInfo["uid"] + " - Đã ngưng chạy!")
                            return True
                        updateStatusBarAccount(user, userInfo['xu'], getFullInfoFB['proxy'], getFullInfo["uid"], f'Đang làm job - {job["id"]}')
                    
                        if fb_feeding:
                            randomAction = random.choice(feedingFunction)
                            print(randomAction)
                        
                            if randomAction == 'Search':
                                obj = Search.Action(chrome)
                                obj.searchInHome(after_sync_to_click_uri=job["link"])
                            elif randomAction == 'Surfing':
                                obj = Surfing.Action(chrome)
                                listSurfing = ['surfing_fbwatch', 'surfing_group_feed', 'surfing_news_feed']
                                randSurfing = random.choice(listSurfing)
                                if randSurfing == 'surfing_fbwatch':
                                    obj.surfing_fbwatch(
                                        surfing_second_min=3,
                                        surfing_second_max=5,
                                        watch_time_min=5,
                                        watch_time_max=10,
                                        after_watch_to_click=job["link"]
                                    )
                                elif randSurfing == 'surfing_group_feed':
                                    obj.surfing_group_feed(
                                        after_suring_to_click_uri=job["link"]
                                    )
                                elif randSurfing == 'surfing_news_feed':
                                    obj.surfing_news_feed(
                                        after_suring_to_click_uri=job["link"]
                                    )
                            elif randomAction == 'Messenger':
                                obj = Messenger.Action(chrome)
                                obj.messageRandomFriend(
                                    after_sync_to_click_uri =job["link"]
                                )
            
                            if actionFB.LikePostMFacebook('', direct=True):
                                updateStatusBarAccount(user, userInfo['xu'], getFullInfoFB['proxy'], getFullInfo["uid"], f'Đã like thành công!')
                                if claim_job.claim_like_vip(job["id"]) == '2':
                                    updateStatusBarAccount(user, userInfo['xu'], getFullInfoFB['proxy'], getFullInfo["uid"], f'Đã nhận xu thành công!')
                                    currentStt += 1
                                    delay = int(EntryDelayJob.get())
                                    for i in range(delay):
                                        time.sleep(1)
                                        updateStatusBarAccount(user, userInfo['xu'], getFullInfoFB['proxy'], getFullInfo["uid"], f'Đã làm xong job, đang nghỉ {delay-i}s')
                                    time.sleep(10)
                        else:
                            if actionFB.LikePostMFacebook(job["link"]):
                                updateStatusBarAccount(user, userInfo['xu'], getFullInfoFB['proxy'], getFullInfo["uid"], f'Đã like thành công!')
                                if claim_job.claim_like_vip(job["id"]) == '2':
                                    updateStatusBarAccount(user, userInfo['xu'], getFullInfoFB['proxy'], getFullInfo["uid"], f'Đã nhận xu thành công!')
                                    currentStt += 1
                                    delay = int(EntryDelayJob.get())
                                    for i in range(delay):
                                        time.sleep(1)
                                        updateStatusBarAccount(user, userInfo['xu'], getFullInfoFB['proxy'], getFullInfo["uid"], f'Đã làm xong job, đang nghỉ {delay-i}s')
                                    time.sleep(10)
                           

                    userInfo = setNick.getInfo()
                  
                    delayjob = int(EntryDelay.get())
                    for i in range(delayjob):
                        time.sleep(1)
                        updateStatusBarAccount(user, userInfo['xu'], getFullInfoFB['proxy'], getFullInfo["uid"], f'Đã làm hết job, đang nghỉ {delayjob-i}s')
                    time.sleep(10)

            except:
                updateMessage('Đang xảy ra lỗi gì đó')
                error += 1
                if error >= 3:
                    updateMessage('Đã xảy ra lỗi 3 lần, dừng chạy')
                    return False
              
                time.sleep(60)
                
def delete (user):
    currentSelect = listbox.curselection()

    if currentSelect:

        item = listbox.get(currentSelect[0])
        # get user
        user = item.split(' - ')[0]
        connection.removeTDSAccount(user)
        messagebox.showinfo("Thông báo", "Xóa thành công") 
        reloadList()

def stop ():
    global userDirector
    currentSelect = listbox.curselection()

    if currentSelect:
        user = listbox.get(currentSelect[0]).split(' - ')[1].split(' - ')[0]
        userDirector[user] = True
        messagebox.showinfo("Thông báo", "Đã gửi lệnh ngưng chạy")

def onListboxSelect(event):
    global userDirector
    currentSelect = listbox.curselection()

    if currentSelect:

        item = listbox.get(currentSelect[0])
        # get user
        user = item.split(' - ')[0]
       
        menu = Menu(window, tearoff=0)
        menu.add_command(label=f"Check đăng nhập TDS ({user})", command=checkLogin)
        userDirector[user] = False
        menu.add_command(label=f"Chạy ({user})", command=lambda: threading.Thread(target=run).start())
        menu.add_command(label=f"Xóa ({user})", command=lambda: delete(user))
        menu.add_command(label=f"Stop ({user})", command=lambda: stop())
        # menu.add_command(label=f"Xem chi tiết {uid}", command=viewInfo)
        # menu.add_command(label=f"Sửa {uid}", command=edit)
        # menu.add_command(label=f"Xóa {uid}", command=remove)
        
        # menu.add_command(label=f"Mở tài khoản {uid}", command=lambda: threading.Thread(target=openAccount).start())
        menu.post(event.x_root, event.y_root)

listbox.bind('<Button-3>', onListboxSelect)
reloadList(reload_first=True)
# loop
window.mainloop()


