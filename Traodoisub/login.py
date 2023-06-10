import requests

class session:
    def __init__(self, user: str, pasw: str, proxy: str = ''):
        self.user = user
        self.pasw = pasw
        self.proxy = proxy
    def login (self) -> dict:
        headers = {
            'authority': 'traodoisub.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'vi,en;q=0.9,en-US;q=0.8,ja;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': 'PHPSESSID=e26c68b1e89ffab62053b2539625158d',
            'origin': 'https://traodoisub.com',
            'referer': 'https://traodoisub.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.41',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'username': self.user,
            'password': self.pasw
        }

        response = requests.post('https://traodoisub.com/scr/login.php', headers=headers, data=data, proxies={
            'http': 'http://'+self.proxy,
        })
        try:
            if response.json()["success"]:
                return response.cookies.get_dict()
            else:
                return False
        except:
            return False