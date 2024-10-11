from requests_html import AsyncHTMLSession
import asyncio
from bs4 import BeautifulSoup


def egydead_extract(self,url,text):
        r = requests.get(url)
        soup = BeautifulSoup(r.content,"html.parser")
        extract = soup.find("div",class_="single-thumbnail")
        tag = extract.find("img")

        if text == "img":
            return tag.get("src")
        elif text == "title":
            return tag.get("alt")


async def egydead_first(url):
    headers = {
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'accept-language': 'ar-EG,ar;q=0.9',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        '___internal-request-id': 'b35fc36c-d361-4fc3-86ca-7b4a5ab261e1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://a120.egyrbyeteuh.sbs',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip',
        #'referer': 'https://a120.egyrbyeteuh.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-boys-%d9%85%d9%88%d8%b3%d9%85-%d8%b1%d8%a7%d8%a8%d8%aa%d8%a9-8/',
    }

    data = {
        'View': '1'  
    }
    session = AsyncHTMLSession()
    response = await session.post(url, headers=headers, data=data)

    #print(response.text)

    soup = BeautifulSoup(response.text,"html.parser")

    eps_list = soup.find("div",class_="EpsList").find_all("a")
    eps_list_links = [x.get("href") for x in eps_list]
    #print(eps_list_links)
    
    if "كامل" in egydead().egydead_extract(url,"title"):
        pass
    else:
        eps_list_links.append(url)
    
    return eps_list_links

async def egydead_second(s,url,res):
    headers = {
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'accept-language': 'ar-EG,ar;q=0.9',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        '___internal-request-id': 'b35fc36c-d361-4fc3-86ca-7b4a5ab261e1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://a120.egyrbyeteuh.sbs',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip',
        #'referer': 'https://a120.egyrbyeteuh.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-the-boys-%d9%85%d9%88%d8%b3%d9%85-%d8%b1%d8%a7%d8%a8%d8%aa%d8%a9-8/',
    }

    data = {
        'View': '1'  
    }
    #session = AsyncHTMLSession()
    response = await s.post(url, headers=headers, data=data)

    soup = BeautifulSoup(response.text,"html.parser")


    servers_list = soup.find("ul",class_="donwload-servers-list").find_all("a")
    servers_list_links = [x.get("href") for x in servers_list]
    first_server = servers_list_links[0]
    
    try:
        download_server_response = await s.get(first_server)
        soup = BeautifulSoup(download_server_response.text,"html.parser")
        first_down_button = soup.find("a",class_="btn btn-primary submit-btn").get("href")
        next_link = "https://gsfqzmqu.sbs/"+first_down_button
        if res == "720p":
            next_link = next_link+"_h"
        elif res == "1080p":
            next_link = next_link+"_x"
    except:
        #await egydead_second(s,url,res)
        next_link = f"{first_server} - ERROR"

    return next_link

async def organizer(url,res):
    eps = await egydead_first(url)
    s= AsyncHTMLSession()
    l = [egydead_second(s,e,res) for e in eps]
    return await asyncio.gather(*l)

def egydead_download(url,res="720p"):
    return asyncio.run(organizer(url,res))



# url = 'https://a120.egyrbyeteuh.sbs/episode/%d9%85%d8%b3%d9%84%d8%b3%d9%84-house-of-the-dragon-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%ab%d8%a7%d9%86%d9%8a-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-8-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/'
# print(egydead_download(url))
