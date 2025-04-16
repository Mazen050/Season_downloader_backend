import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time

def searcharab(search_term,catagory="series"):
    url = "https://m15.asd.rest/wp-content/themes/Elshaikh2021/Ajaxat/SearchingTwo.php"

    form_data = {
        'search': search_term,
        'type': catagory,
    }

    r = requests.post(url,data=form_data)
    response = r.content.decode("utf-8")
    soup = BeautifulSoup(response,"html.parser")
    results = soup.find_all("a")

    combo = [[l.find("h4").text,l.find("img").get("data-image"),l.get("href")] for l in results]

    return combo

async def arabseed_ep(url):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            soup = BeautifulSoup(await r.text(),"html.parser")
            downloadep = soup.find("a",class_="downloadBTn").get("href")
            headers = {
                "referer":"https://m15.asd.rest/",
            }
            async with s.get(downloadep,headers=headers) as r1:
                soup = BeautifulSoup(await r1.text(),"html.parser")
                # arabseedservers = soup.find_all("a",class_="downloadsLink HoverBefore ArabSeedServer")
                HQserver = soup.find("a",class_="downloadsLink HoverBefore ArabSeedServer").get("href")
                headers = {
                "referer":downloadep,
                }   
                async with s.get(HQserver,headers=headers) as r2:
                    res = str(await r2.text()).split('"')
                    link = [re for re in res if "https" in re]
                    async with s.get(link[0]) as r2_5:
                        soup = BeautifulSoup(await r2_5.text(),"html.parser")
                        next= soup.find("a",class_="downloadbtn").get("href")
                        async with s.get(next) as r3:
                            soup = BeautifulSoup(await r3.text(),"html.parser")
                            directDownloadLink= soup.find("a",class_="downloadbtn").get("href")
                            return [directDownloadLink,directDownloadLink.split("/")[-1]]




async def arabseed_async(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")
    epslist = soup.find("div",class_="ContainerEpisodesList")
    links = epslist.find_all("a")
    tasks = [arabseed_ep(url.get("href")) for url in links]
    return await asyncio.gather(*tasks)

def arabseed_download(url):
    return asyncio.run(arabseed_async(url))

