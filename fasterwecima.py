import requests
import aiohttp
from bs4 import BeautifulSoup
import asyncio


async def episode(link):
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(link) as r:
                soup = BeautifulSoup(await r.text(),"html.parser")
                downloadList = soup.find("ul",class_="List--Download--Wecima--Single")
                downloads = downloadList.find_all("a",class_="hoverable activable")
                for download in downloads:
                    if "720p" in download.find("resolution").text:
                        return download.get("href")
                return "No 720p quality found"
        except Exception as e:
            print(e)
            return


async def wecimascraper_async(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content,"html.parser")
    eps_list = soup.find("div",class_="Episodes--Seasons--Episodes").find_all("a")
    epsLinks = [x.get("href") for x in eps_list]
    tasks = [episode(x) for x in epsLinks]
    return await asyncio.gather(*tasks)

def wecimascraper(link):
    return asyncio.run(wecimascraper_async(link))


