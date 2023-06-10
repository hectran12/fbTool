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

from chrome import helper

# Tiknter import
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext

db = connection.getCol()
if db != None:
    print(color.green, 'Kết nối database thành công', color.end)
else:
    print(color.red, 'Kết nối database thất bại', color.end)
    sys.exit()


ultis.clear()


config = conf.config



# create form
window = Tk()
window.title("Danh sách tài khoản FACEBOOK")
window.geometry('500x500')
countAccountFB = len(connection.getAllAccountFB())
countAccountFBLive = connection.getCountAccountFBLive()
countAccountFBDie = countAccountFB - countAccountFBLive
labelCountAccount = Label(window, text=f'Tổng số tài khoản: {countAccountFB}')
labelCountAccount.pack()
labelCountAccountLive = Label(window, text=f'Tổng số tài khoản sống: {countAccountFBLive}')
labelCountAccountLive.pack()
labelCountAccountDie = Label(window, text=f'Tổng số tài khoản chết: {countAccountFBDie}')
labelCountAccountDie.pack()



# create list
listbox = Listbox(window, width=150, height=150)




def reloadList():
    # clear item in listbox
    listbox.delete(0, END)

    # print all account with info
    accounts = connection.getAllAccountFB()
    for acc in accounts:
        outAcc = f'[{accounts.index(acc) + 1}] UID: {acc["uid"]} | password: {acc["password"]}'
        if 'info' in acc:
            outAcc += f' | name: {acc["info"]["name"]}'
        
        
        listbox.insert(END, outAcc)
    countAccountFB = len(connection.getAllAccountFB())
    countAccountFBLive = connection.getCountAccountFBLive()

    # UPDATE LABEL
    labelCountAccount.config(text=f'Tổng số tài khoản: {countAccountFB}')
    labelCountAccountLive.config(text=f'Tổng số tài khoản sống: {countAccountFBLive}')
    labelCountAccountDie.config(text=f'Tổng số tài khoản chết: {countAccountFB - countAccountFBLive}')

# button reload
buttonReload = Button(window, text="Tải lại", command=reloadList)
buttonReload.pack()  




listbox.pack()
reloadList()


def onListboxSelect(event):
    currentSelect = listbox.curselection()

    if currentSelect:

        item = listbox.get(currentSelect[0])
        # get uid
        uid = item.split('UID: ')[1].split(' |')[0]
       
        menu = Menu(window, tearoff=0)
        menu.add_command(label=f"Xem chi tiết {uid}", command=viewInfo)
        menu.add_command(label=f"Sửa {uid}", command=edit)
        menu.add_command(label=f"Xóa {uid}", command=remove)
        
        menu.add_command(label=f"Mở tài khoản {uid}", command=lambda: threading.Thread(target=openAccount).start())
        menu.post(event.x_root, event.y_root)


def viewInfo ():
    currentSelect = listbox.curselection()

    if currentSelect:

        item = listbox.get(currentSelect[0])
        # get uid
        uid = item.split('UID: ')[1].split(' |')[0]
        getFullInfo = connection.getAccountFB(uid)

        result = ''
        for key, value in getFullInfo.items():
            if key != 'password':
                result += f'{key}: {value}\n'
        
        messagebox.showinfo(f'Chi tiết tài khoản {uid}', result)


def edit ():
    currentSelect = listbox.curselection()

    if currentSelect:

        item = listbox.get(currentSelect[0])
        # get uid
        uid = item.split('UID: ')[1].split(' |')[0]
        getFullInfo = connection.getAccountFB(uid)

        # mini form
        miniForm = Tk()
        miniForm.title(f"Sửa tài khoản {uid}")
        miniForm.geometry('500x500')
        entrs = []
        for name, value in getFullInfo.items():
            Label(miniForm, text=name).pack()
            entr = Entry(miniForm, width=50)
            entr.insert(0, value)
            entr.tag = name
            entr.type = type(value)
            entr.pack()
            entrs.append(entr)
      
        Button(miniForm, text='Lưu', command=lambda: 
            [connection.reUpdateAccountFB(uid, entrs),
            messagebox.showinfo('Thông báo', 'Chỉnh sửa thành công'),
            reloadList(),
            miniForm.destroy() # close form

            ]
        ).pack()
        miniForm.mainloop()


def openAccount():
    currentSelect = listbox.curselection()

    if currentSelect:

        item = listbox.get(currentSelect[0])
        # get uid
        uid = item.split('UID: ')[1].split(' |')[0]

        getFulllInfo = connection.getAccountFB(uid)
        if 'info' in getFulllInfo:
            headless = False
            if config.get('chrome_setting', 'headless_mode') == '1':
                headless = True
            driver = helper.createDriver(profile_path=getFulllInfo["profile_path"], 
                                path_driver=config.get('chrome_setting', 'chromedriver_path'),
                                  headless_mode=headless,
                                    proxy=getFulllInfo["proxy"])
            # create panel form
            panelForm = Tk()
            panelForm.title(f"Tài khoản {uid}")
            panelForm.geometry('150x150')
            # create label
            labelName = Label(panelForm, text=f'Tên: {getFulllInfo["info"]["name"]}')
            labelName.pack()
            labelAnotherFunction = Label(panelForm, text=f'Chức năng khác: ')
            labelAnotherFunction.pack()
            buttonDirectToFB = Button(panelForm, text="Truy cập facebook", command=lambda: driver.get('https://facebook.com'))
            buttonDirectToFB.pack()
            buttonCloseTab = Button(panelForm, text="Đóng tab", command=lambda: driver.close())
            buttonCloseTab.pack()
            buttonCloseAllTab = Button(panelForm, text="Đóng tất cả tab", command=lambda: driver.quit())
            buttonCloseAllTab.pack()
           
            
            buttonCloseForm = Button(panelForm, text="Đóng", command=lambda: panelForm.destroy())
            buttonCloseForm.pack()
            # loop
            panelForm.mainloop()

        else:
            print(color.red, 'Tài khoản chưa có thông tin, chưa tạo profile', color.end)

def remove ():
    currentSelect = listbox.curselection()

    if currentSelect:

        item = listbox.get(currentSelect[0])
        # get uid
        uid = item.split('UID: ')[1].split(' |')[0]
        connection.removeAccountFB(uid)
        messagebox.showinfo('Thông báo', 'Xóa thành công')
        reloadList()

        
listbox.bind('<Button-3>', onListboxSelect)

# loop
window.mainloop()
    
