import requests
from requests_html import AsyncHTMLSession
import asyncio
import time
from bs4 import BeautifulSoup

class akwamscrape():
    def epdown(self,url=""):
        self.url = url

        r= requests.get(url)
        self.soup = BeautifulSoup(r.content,"html.parser")
        epslist = self.soup.find_all('div',class_='bg-primary2 p-4 col-lg-4 col-md-6 col-12')
        self.eplinks=[]

        for i in epslist:
            y = i.find('a')
            x = y.get('href')
            self.eplinks.append(x)
        self.eplinks = self.eplinks[::-1]

    async def scrape(self,s,url):
        downloadL = []
        ep = await s.get(url)
        ep_soup = BeautifulSoup(ep.html.html,"html.parser")
        res = ep_soup.find("ul",class_="header-tabs tabs d-flex list-unstyled p-0 m-0")
        x = ep_soup.find_all('a',class_="link-btn link-download d-flex align-items-center px-3")
        if res.find("li").find("a").text == "1080p":
            y = x[1].get('href')
        else:
            y = x[0].get("href")
        downloadL.append(y)

        clickhere = []
        ep=await s.get(y)
        ep_soup = BeautifulSoup(ep.html.html,"html.parser")
        x = ep_soup.find('a',class_="download-link")
        y = x.get('href')
        clickhere.append(y)

        downlinks = []
        ep=await s.get(y)
        ep_soup = BeautifulSoup(ep.html.html,"html.parser")
        x = ep_soup.find('a',class_="link btn btn-light")
        y = x.get('href')
        if "720p" in y:
            downlinks.append(y)
        else:
            downlinks.append("Couldnt find 720p res")
        #print(y)
        return y
        

    async def gather(self,url):
        self.epdown(url)
        s = AsyncHTMLSession()
        tasks = [self.scrape(s,url) for url in self.eplinks]
        return await asyncio.gather(*tasks)
    

    def getDLL(self,url):
        y = asyncio.run(self.gather(url))
        return y
    
    async def search(self, text):
        url = "https://ak.sv/search?q="
        search = ""
        if " " in text:
            for word in text:
                if word == " ":
                    search += "+"
                else:
                    search += word
        else:
            search = text
        url += search
        r = requests.get(url)
        soup = BeautifulSoup(r.content,"html.parser")
        results = soup.find("div",class_="widget-body row flex-wrap")
        seasons = results.find_all("div",class_="entry-box entry-box-1")
        async def searchitems(html):
            combo = []
            soup = BeautifulSoup(html,"html.parser")
            imglink = soup.find("img").get("data-src")
            href = soup.find("h3").a.get("href")
            title = soup.find("h3").a.text
            combo.append(title)
            combo.append(imglink)
            combo.append(href)
            return combo
        tasks = [searchitems(str(html)) for html in seasons]
        return await asyncio.gather(*tasks)


    def akwamsearch(self, text):
        return asyncio.run(self.search(text))

#start = time.perf_counter()
#x = akwamscrape()
#y = x.akwamsearch("peaky blinders")
#print(y)
#for i in y:
#    print(i)
#    print("-----------------------------------------------------------------------------")
#print(len(y))

#y = asyncio.run(x.getDLL())
#print(y)
#print(time.perf_counter()-start)
