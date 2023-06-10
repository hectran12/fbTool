from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

class Action:
    def __init__ (self, driver: webdriver.Chrome):
        self.driver = driver

    def LikePostMFacebook (self, url: str, direct=False) -> bool:
        if direct == False:
            self.driver.get(url)
        idFBAction = self.driver.page_source.split('<div id="')[1].split('"')[0].strip()
       
        listElement = [
            f'//*[@id="{idFBAction}"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]',
            f'//*[@id="watch_feed"]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div[1]/div/div[1]',
            f'//*[@id="{idFBAction}"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]',
            f'//*[@id="{idFBAction}"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]',
            f'//*[@id="{idFBAction}"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]',
            f'//*[@id="{idFBAction}"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div[1]/div',
            f''
        ]

        for element in listElement:
            try:
      
                self.driver.find_element('xpath', element).click()
                time.sleep(2)
                return True
            except:
                pass
