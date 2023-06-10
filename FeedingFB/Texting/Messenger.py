from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys
import random
sys.path.append('./FeedingFB')
from Hand_gestures import Surfing
sys.path.append('./')
from AI import train

import time
import random
class Action:
    def __init__ (self, driver: webdriver.Chrome):
        self.driver = driver

    def messageRandomFriend (self, message_count_min=1, message_count_max=3, after_sync_to_click_uri=''):
        try:
            self.driver.get('https://m.facebook.com/messages/')
            time.sleep(2)
            # get list friend
            listfriend = self.driver.execute_script('return document.querySelector("#threadlist_rows").outerHTML;')
            listfriend = listfriend.split('<a href="')
            messageLinkFriend = []
            for link in listfriend:
                if 'messages' in link:
                    messageLinkFriend.append(link.split('"')[0])
            if len(messageLinkFriend) > 0:
                linkFriend = random.choice(messageLinkFriend)
                js_execute = f'''
                    html = `<a href="{linkFriend}" class="_5b6s" id="selecter">Ngô Lê Nguyệt Lan</a>`
                    document.querySelector("#threadlist_rows").innerHTML += html;
                    // click
                    document.querySelector("#selecter").click();
                '''
                self.driver.execute_script(js_execute)

                time.sleep(2)
                for i in range(random.randint(message_count_min, message_count_max)):
                    content = train.randomMessageVietnamese()
                    self.driver.find_element('id', 'composerInput').send_keys(content+'\n')
                    time.sleep(random.randint(1, 5))
                    self.driver.find_element('name', 'send').click()

                if after_sync_to_click_uri  == '':
                    return True
                
                time.sleep(2)
                js_add_tag_a = f'''
                    html = `<a id="requireClick" aria-label="Mann up" class="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz xzsf02u x1rg5ohu" href="{after_sync_to_click_uri}" role="link" tabindex="0"><div class="x1rg5ohu x1n2onr6 x3ajldb x1ja2u2z"><svg aria-hidden="true" class="x3ajldb" data-visualcompletion="ignore-dynamic" role="none" style="height: 40px; width: 40px;"><mask id=":r76:"><circle cx="20" cy="20" fill="white" r="20"></circle></mask><g mask="url(#:r76:)"><image x="0" y="0" height="100%" preserveAspectRatio="xMidYMid slice" width="100%" xlink:href="https://scontent.fsgn5-14.fna.fbcdn.net/v/t39.30808-1/335990189_579870140740831_7258936613613283976_n.jpg?stp=c0.0.40.40a_cp0_dst-jpg_p40x40&amp;_nc_cat=1&amp;ccb=1-7&amp;_nc_sid=c6021c&amp;_nc_ohc=G3YlLe38hRwAX_s5DJO&amp;_nc_ht=scontent.fsgn5-14.fna&amp;oh=00_AfAryG8V1Q1iU3kKe_YUkn2Dtw5V2-PR7Kk8c-aEYOPUxg&amp;oe=6486C5AC" style="height: 40px; width: 40px;"></image><circle class="xbh8q5q x1pwv2dq xvlca1e" cx="20" cy="20" r="20"></circle></g></svg><div class="x1ey2m1c xds687c xg01cxk x47corl x10l6tqk x17qophe x13vifvy x1ebt8du x19991ni x1dhq9h x1wpzbip x14yjl9h xudhj91 x18nykt9 xww2gxu" data-visualcompletion="ignore"></div></div></a>`;
                    document.body.innerHTML += html;
                
                    document.getElementById('requireClick').click();


                '''
                self.driver.execute_script(js_add_tag_a)
                return True
            else:
                return True
        except:
            if after_sync_to_click_uri  == '':
                return False
            js_add_tag_a = f'''
                html = `<a id="requireClick" aria-label="Mann up" class="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz xzsf02u x1rg5ohu" href="{after_sync_to_click_uri}" role="link" tabindex="0"><div class="x1rg5ohu x1n2onr6 x3ajldb x1ja2u2z"><svg aria-hidden="true" class="x3ajldb" data-visualcompletion="ignore-dynamic" role="none" style="height: 40px; width: 40px;"><mask id=":r76:"><circle cx="20" cy="20" fill="white" r="20"></circle></mask><g mask="url(#:r76:)"><image x="0" y="0" height="100%" preserveAspectRatio="xMidYMid slice" width="100%" xlink:href="https://scontent.fsgn5-14.fna.fbcdn.net/v/t39.30808-1/335990189_579870140740831_7258936613613283976_n.jpg?stp=c0.0.40.40a_cp0_dst-jpg_p40x40&amp;_nc_cat=1&amp;ccb=1-7&amp;_nc_sid=c6021c&amp;_nc_ohc=G3YlLe38hRwAX_s5DJO&amp;_nc_ht=scontent.fsgn5-14.fna&amp;oh=00_AfAryG8V1Q1iU3kKe_YUkn2Dtw5V2-PR7Kk8c-aEYOPUxg&amp;oe=6486C5AC" style="height: 40px; width: 40px;"></image><circle class="xbh8q5q x1pwv2dq xvlca1e" cx="20" cy="20" r="20"></circle></g></svg><div class="x1ey2m1c xds687c xg01cxk x47corl x10l6tqk x17qophe x13vifvy x1ebt8du x19991ni x1dhq9h x1wpzbip x14yjl9h xudhj91 x18nykt9 xww2gxu" data-visualcompletion="ignore"></div></div></a>`;
                document.body.innerHTML += html;
            
                document.getElementById('requireClick').click();


            '''
            self.driver.execute_script(js_add_tag_a)
            return False
