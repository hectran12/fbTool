import sys
sys.path.append('./')
from loader import color
from loader import conf
from loader import ultis
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

def createDriver(profile_path: str, path_driver: str, headless_mode: bool, proxy: str='') -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    pathExtensionPack = conf.config.get('chrome_setting', 'extension_pack_path')
    proxyExtension = pathExtensionPack + '\\Proxy-Helper.crx'
    #options
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    
    if headless_mode:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    
    options.add_experimental_option("prefs", {"credentials_enable_service": False})
    options.add_experimental_option("prefs", {"profile.password_manager_enabled": False})
    setupProxy = True
    if proxy != '':
        if '@' not in proxy:
            print('Debug: No proxy')
            # set proxy
            options.add_argument('--proxy-server=%s' % proxy)
        else:
            # add extension Proxy-Helper.crx
            print('Debug: proxy here')
            options.add_extension(proxyExtension)
            setupProxy = True


    
    options.add_argument("--disable-infobars")
    # usage profile
    options.add_argument("--user-data-dir=" + profile_path)
    driver = webdriver.Chrome(options=options, executable_path=path_driver)
    if setupProxy:
        driver.get('chrome-extension://hheejnkdpbnlbppabadgboahgjdikacj/options.html')
        proxySplit = proxy.split('@')
        authen = proxySplit[0].split(':')
        access = proxySplit[1].split(':')

        # set proxy
        driver.find_element('id', 'http-host').send_keys(access[0])
        driver.find_element('id', 'http-port').send_keys(access[1])

        # set authen
        driver.find_element('id', 'username').send_keys(authen[0])
        driver.find_element('id', 'password').send_keys(authen[1] + '\n')

        time.sleep(1)
        driver.get('chrome-extension://hheejnkdpbnlbppabadgboahgjdikacj/popup.html')
   
    return driver