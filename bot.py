import requests
import json
import os
import urllib.parse
from colorama import *
from datetime import datetime
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class RatsKingdom:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'app.ratskingdom.com',
            'Origin': 'https://d1tt9nsj36gcwe.cloudfront.net',
            'Pragma': 'no-cache',
            'Referer': 'https://d1tt9nsj36gcwe.cloudfront.net/?tgWebAppStartParam=1493482017',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Rats Kingdom - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_data(self, query: str) -> dict:
        parsed_query = urllib.parse.parse_qs(query)
        user_data = json.loads(parsed_query['user'][0])
        telegram_id = user_data['id']
        data = {
            "isPremium": False,
            "parentRefId": "1493482017",
            "refBonus": 0,
            "telegramId": telegram_id,
            "username": user_data['username']
        }

        return {"data":data, "telegram_id":telegram_id}

    def user_login(self, query: str):
        url = 'https://app.ratskingdom.com/api/v1/user'
        data = json.dumps({"initData":query, "user":self.load_data(query)['data']})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 201:
            return response.json()
        else:
            return None

    def user_data(self, telegram_id: int, query: str):
        url = f'https://app.ratskingdom.com/api/v1/user/{telegram_id}/telegramId'
        data = json.dumps({"initData":query})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 201:
            return response.json()
        else:
            return None

    def check_tasks(self, task_id: str, user_id: str, type: str):
        url = f'https://app.ratskingdom.com/api/v1/task/{task_id}/{user_id}/check'
        data = json.dumps({"taskType":type})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 201:
            return response.json()
        else:
            return None

    def claim_tasks(self, task_id: str, telegram_id: int):
        url = f'https://app.ratskingdom.com/api/v1/user/claimTaskById'
        data = json.dumps({"taskId":task_id, "telegramId":telegram_id})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.session.patch(url, headers=self.headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def process_query(self, query: str):
        telegram_id = self.load_data(query)['telegram_id']

        user = self.user_data(telegram_id, query)
        if not user:
            login = self.user_login(query)
            if login:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {login['username']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Status{Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT} Login Successfully {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Query May Expired {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                return
            
            user = self.user_data(telegram_id, query)

        if user:
            user_id = user['_id']
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['username']} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['tokens']} RATS {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
            time.sleep(1)

            tasks = user['taskRefs']
            if tasks:
                for task in tasks:
                    task_id = task['_id']
                    type = task['taskRef']['type']
                    status = task['status']

                    if task and status == 'incomplete':
                        check = self.check_tasks(task_id, user_id, type)
                        if check:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['taskRef']['title']} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                            time.sleep(1)

                            claim = self.claim_tasks(task_id, telegram_id)
                            if claim and claim['task']['status'] == 'claimed':
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['taskRef']['title']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {claim['task']['taskRef']['reward']} RATS {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['taskRef']['title']} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['taskRef']['title']} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        time.sleep(1)

                    elif task and status == 'completed':
                        claim = self.claim_tasks(task_id, telegram_id)
                        if claim and claim['task']['status'] == 'claimed':
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['taskRef']['title']} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {claim['task']['taskRef']['reward']} RATS {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['taskRef']['title']} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        time.sleep(1)
            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )

    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        time.sleep(3)

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Rats Kingdom - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = RatsKingdom()
    bot.main()