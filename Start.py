import requests, json, threading,os,time,datetime # Importing Modules
from Utils.CharacterGen import Email, Username, Password # Importing Classes

from colorama import Fore, init
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from datetime import datetime
from colorama import init, Fore 


software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.LINUX.value]   
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
user_agent = user_agent_rotator.get_random_user_agent()
init()
headers = {
    'authority': 'www.guilded.gg',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'guilded-viewer-platform': 'desktop',
    'origin': 'https://www.guilded.gg',
    'referer': 'https://www.guilded.gg/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': user_agent,
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'type': 'email',
}

init(autoreset=True)
r = Fore.RESET
lr = Fore.LIGHTRED_EX
g = Fore.GREEN
y = Fore.YELLOW
w = Fore.WHITE

def currentTime(color):
    return datetime.now().time().strftime(f"{color}%H:{color}%M:{color}%S{r}")
class console:
    def success(text):
        print(f"[{currentTime(g)}]{Fore.WHITE} {text}")
    def info(text):
        print(f"[{currentTime(y)}]{Fore.WHITE} {text}")
    def error(text):
        print(f"[{currentTime(lr)}]{Fore.WHITE} {text}")


class AccountMaker:
    
    def __init__(self):
        
        # Reading Config.json and getting the data  
        f = open("RaiderConfig.json")
        data = json.load(f)
        
        # Checking if we want the username to be realistic
        if data["Realistic"] == "true":
            self.username = Username(True)
        else:
            self.username = Username(False)
            
        # Setting the password and email
        self.password = Password()
        self.email = Email()
        
        # Server Invite Code
        self.invite = data["Invite"]
        # User Token
        self.token = ''
        
        self.Stage1()
    
    def Stage1(self):
        
        json_data = {
            'extraInfo': {
                'platform': 'desktop',
            },
            'name': self.username,
            'email': self.email,
            'password': self.password,
            'fullName': self.username,
        }   
        
        r = requests.post('https://www.guilded.gg/api/users', params=params, headers=headers, json=json_data)
        
        
        if r.status_code != 200:
            console.error(f"{w}[{lr}Stage 1 Failed{w}] Failed to make account : {r.json()}")
        else:
            self.token = r.cookies.get('hmac_signed_session')
            console.success(f"{w}[{g}Stage 1 Completed{w}] Account Generated Successfully [{self.username}:{self.token[:15]}]")  # : P {self.password} : E {self.email}
            
            self.Stage2()
        
   
    
    def Stage2(self):
        r = requests.put("https://www.guilded.gg/api/invites/" + self.invite, json={"type": "consume"}, cookies={"hmac_signed_session": self.token})
        
        if r.status_code == 200:
            
            console.success(f"{w}[{g}Stage 2 Completed{w}] {Fore.WHITE}Joined Server Successfully") # : https://www.guilded.gg/i/{self.invite}
            self.Stage3()
        else:
            console.error(f"{w}[{lr}Stage 2 Failed{w}] {Fore.WHITE}Failed to Join : {r.json()}")
        
        
    
    def Stage3(self):
        r = requests.put('https://www.guilded.gg/api/users/me/ping', cookies={"hmac_signed_session": self.token})
        
        if r.status_code == 200:
            console.success(f"{w}[{g}Stage 3 Completed{w}] {Fore.WHITE}Ping Req Successful")
            self.Stage4()
        else:
            console.error(f"{w}[{lr}Stage 3 Failed{w}] {Fore.WHITE}Ping Req Failed")

    def Stage4(self):
        presentDate = datetime.now()
        unix_timestamp = datetime.timestamp(presentDate)*1000
        json_data = {
            'data': [
                {
                    'time': unix_timestamp,
                    'eventSource': 'Client',
                    'eventName': 'TimeSpent',
                    'viewerPlatform': 'desktop',
                    'viewerAppType': 'None',
                    'viewerSystemName': 'Win32',
                    'browser': 'Chrome',
                    'device': None,
                    'attributionSource': 'YouTube',
                    'gitHash': '5bfbaea5',
                },
            ],
        }

        r = requests.put('https://www.guilded.gg/api/data/event', cookies={"hmac_signed_session": self.token},  json=json_data)
        
        if r.status_code == 200:
            console.success(f"{w}[{g}Stage 4 Completed{w}] {Fore.WHITE}Event/HeartBeat Req Successful")
        else:
            console.error(f"{w}[{lr}Stage 4 Failed{w}] {Fore.WHITE}Event/HeartBeat Req Failed")


threads = []
os.system('cls')
user_treads = int(input("Threads (no more than 3 or rateLimit/ipban) >> "))
try:
    for _ in range(user_treads):
        thread = threading.Thread(target=AccountMaker, daemon=True)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
except KeyboardInterrupt:
    exit()
except: 
    pass
