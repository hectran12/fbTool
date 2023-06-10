import sys
sys.path.append('./')
from loader import color
from loader import conf
from loader import ultis
from chrome import helper
from database import connection
from AI import train
# date time
import datetime
import time
# threading
import threading
sys.path.append('./FeedingFB')
from Hand_gestures import Surfing
from Hand_gestures import Search
from Texting import Messenger
import time
import datetime
db = connection.getCol()
if db != None:
    print(color.green, 'Kết nối database thành công', color.end)
else:
    print(color.red, 'Kết nối database thất bại', color.end)
    sys.exit()

config = conf.config
ultis.clear()


getFullInfoFB = connection.getAccountFB('100092868720659')
chrome = helper.createDriver(profile_path=getFullInfoFB["profile_path"], 
                                path_driver=config.get('chrome_setting', 'chromedriver_path'),
                                  headless_mode=False,
                                    proxy=getFullInfoFB["proxy"])
# surfing = Surfing.Action(chrome)
# surfing.surfing_group_feed()
messenger = Messenger.Action(chrome)
messenger.messageRandomFriend(after_sync_to_click_uri='https://www.facebook.com/profile.php?id=100077557920226')
input()