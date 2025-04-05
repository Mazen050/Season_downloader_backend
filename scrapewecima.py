import requests
from bs4 import BeautifulSoup

def wecimascraper(url):
    try:
        r= requests.get(url)
    except:
        return []
    
    soup = BeautifulSoup(r.content,"html.parser")
    epslist = soup.find('div',class_="Episodes--Seasons--Episodes")
    eps = epslist.find_all('a')
    eplinks=[]

    for i in eps:
        x = i.get('href')
        eplinks.append(x)
    eplinks = eplinks[::-1]

    links=[]
    for i in eplinks:
        link = requests.get(i)
        soup = BeautifulSoup(link.content,"html.parser")
        x= soup.find('ul',class_="List--Download--Wecima--Single")
        y=x.find_all('a',class_="hoverable activable")
        for h in y:
            href = h.get("href")
            res = h.find("resolution").text
            if "720p" in str(res):
                links.append(href)
                #print(href)
            else:
                continue
    return links
        
def wecimatitle(url):
    try:
        r= requests.get(url)
    except:
        return ''
    soup = BeautifulSoup(r.content,"html.parser")
    return soup.find("h1").text

def wecimaimage(url):
    try:
        r= requests.get(url)
    except:
        return ''
    soup = BeautifulSoup(r.content,"html.parser")
    #image = soup.find("div",class_="Poster--Single-begin")
    imgurl = soup.find("wecima",class_="separated--top").get("data-lazy-style")
    if imgurl == None:
        imgurl = soup.find("wecima",class_="separated--top").get("style")
    return imglinkget(imgurl)

def imglinkget(text):
    x=str(text).split("(")
    y = x[1].split(")")
    return y[0]

def wecimasearch(text):
    search = ""
    if " " in text:
            for word in text:
                if word == " ":
                    search += "+"
                else:
                    search += word
    else:
        search = text
    urlseries = "https://wecima.show/search/"+text+"/list/series/"
    urlanime = "https://wecima.show/search/"+text+"/list/anime/"
    combo = []
    def getsearch(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content,"html.parser")
        resultbox = soup.find("div",class_="Grid--WecimaPosts")
        results = resultbox.find_all("div",class_="GridItem")

        for result in results:
            x = result.find("div")
            title = x.a.get("title")
            img = imglinkget(x.span.get("data-lazy-style"))
            href = x.a.get("href")
            l = [title,img,href]
            combo.append(l)
    getsearch(urlseries)
    getsearch(urlanime)
    return combo
def wecimaseasons(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content,"html.parser")
    x = soup.find("div",class_="List--Seasons--Episodes")
    combo = []
    try:
        seasons = x.find_all("a")
    except:
        combo.append(["Season 1",link])
        return combo
    for season in seasons:
        title = season.text
        href = season.get("href")
        l = [title,href]
        combo.append(l)
    return combo


#print(wecimatitle("https://wecima.show/watch/%d9%85%d8%b4%d8%a7%d9%87%d8%af%d8%a9-%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-boys-%d9%85%d9%88%d8%b3%d9%85-4-%d8%ad%d9%84%d9%82%d8%a9-5/"))
#print(wecimaimage("https://wecima.show/watch/%d9%85%d8%b4%d8%a7%d9%87%d8%af%d8%a9-%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-boys-%d9%85%d9%88%d8%b3%d9%85-4-%d8%ad%d9%84%d9%82%d8%a9-5/"))
#print(wecimaimage("https://wecima.show/series/%d9%85%d9%88%d8%b3%d9%85-1-the-boys/"))
#print(wecimasearch("the boys"))
#print(wecimaseasons("https://wecima.show/series/%d9%85%d8%b3%d9%84%d8%b3%d9%84-dexter/"))
#print(wecimascraper("https://wecima.show/series/%d9%85%d9%88%d8%b3%d9%85-2-%d8%a7%d9%84%d8%a8%d9%8a%d8%aa-%d8%a8%d9%8a%d8%aa%d9%8a/"))
