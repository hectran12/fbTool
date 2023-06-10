import requests

class session:
    def __init__ (self, cookies: dict, proxy: str = ''):
        self.cookies = cookies
        self.proxy = {
                'http': 'http://'+proxy
                }
        self.header = {
            'authority': 'traodoisub.com',
            'accept': '*/*',
            'accept-language': 'vi,en;q=0.9,en-US;q=0.8,ja;q=0.7',
            # 'cookie': 'PHPSESSID=e26c68b1e89ffab62053b2539625158d',
            'referer': 'https://traodoisub.com/ex/like/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.41',
        }
    def datnick (self, idfb: str) -> int:
        data = {
            'iddat': idfb,
        }

        response = requests.post('https://traodoisub.com/scr/datnick.php', cookies=self.cookies, headers=self.header, data=data, proxies=self.proxy)
        try:
            if response.text == '1':
                return True
            else:
                return False
        except:
            return False
        
    def getInfo (self) -> dict:
        try:
            response = requests.get('https://traodoisub.com/scr/user.php', cookies=self.cookies, headers=self.header, proxies=self.proxy)
            json = response.json()
            return json
        except:
            return False
