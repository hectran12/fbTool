import sys
sys.path.append('./')
from loader import color
from loader import conf
from loader import ultis
from database import connection


# full import selenium chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# wait element
from selenium.webdriver.support.ui import WebDriverWait
from chrome import helper

import time
import pyotp
#signal
import signal
config = conf.config


class newSession ():
    def __init__(self, uid='', profile_name='', mongo_connection: connection = None):
        self.uid_create = uid
        self.profile_name = profile_name
        self.mongo = mongo_connection
        

    def start(self):
        info_selector = self.mongo.getAccountFB(self.uid_create)
        # create profile
        if self.profile_name == '':
            self.profile_name = info_selector['uid']

        pathDriver = config.get('chrome_setting', 'chromedriver_path')
        if pathDriver == '0':
            pathDriver = ''
        
        profilePath = config.get('local_data', 'profile_chrome_facebook') + '\\' + self.profile_name
        if ultis.checkPath(profilePath) == False:
            ultis.createFolder(profilePath)
        
        useHeadless = False
        if config.get('chrome_setting', 'headless_mode') == '1':
            useHeadless = True

        # check status proxy
        if 'proxy' not in info_selector:
            info_selector['proxy'] = ''
        if info_selector['proxy'] != '':
            proxy = info_selector['proxy']
        else:
            proxy = ''

        
        # create driver

        driver = helper.createDriver(
            profile_path=profilePath,
            path_driver=pathDriver,
            headless_mode=useHeadless,
            proxy=proxy
        )
        


    
        try:
            driver.get('https://facebook.com')
            # wait element email
            WebDriverWait(driver, 10).until(lambda d: driver.find_element('id', 'email'))
            driver.find_element('id', 'email').send_keys(info_selector['uid'])
            driver.find_element('id', 'pass').send_keys(info_selector['password'])
            driver.find_element('name', 'login').click()

            if info_selector["2fa"] != "":
                code_twofa = pyotp.TOTP(info_selector["2fa"]).now()
                WebDriverWait(driver, 10).until(lambda d: driver.find_element('id', 'approvals_code'))
                driver.find_element('id', 'approvals_code').send_keys(code_twofa)
                driver.find_element('id', 'checkpointSubmitButton').click()
                try:
                    driver.find_element('id', 'checkpointSubmitButton').click()
                except:
                    pass
            if driver.page_source.__contains__('https://www.facebook.com/profile.php'):
                print(color.green, 'Đăng nhập thành công', color.end)
                driver.get('https://www.facebook.com/profile.php')
                fbComID = driver.page_source.split('<div id="')[1].split('"')[0]
       
                try:                                            
                    elementToWait = driver.find_element('xpath', f'//*[@id="{fbComID}"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[1]/div[3]/div/div/div[1]/div/div/span/h1')
                    WebDriverWait(driver, 10).until(lambda d: elementToWait)
                    getName = elementToWait.text
                    
             
                except:
                    elementToWait = driver.find_element('xpath', f'//*[@id="{fbComID}"]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[1]/div[3]/div/div/div[1]/div/div/span/h1')
                    WebDriverWait(driver, 10).until(lambda d: elementToWait)
                    getName = elementToWait.text

                print(color.green, 'Tên hiển thị: ', color.end, color.yellow, getName, color.end)
                info = {
                    'uid': info_selector['uid'],
                    'name': getName,
                }
                connection.updateInfoFacebook(info_selector["uid"], info)
                connection.updateProfilePath(info_selector["uid"], profilePath)
                connection.updateStatusAccountFB(info_selector["uid"], True)
                print(color.green, 'Tạo profile thành công', color.end)
              
            else:
                print(color.red, 'Đăng nhập thất bại', color.end)
                connection.updateStatusAccountFB(info_selector["uid"], False)
                driver.quit()
                ultis.removeFolder(profilePath)
        except:
            driver.quit()
            print(color.red, 'Lỗi khi tạo profile', color.end)
            ultis.removeFolder(profilePath)

        
