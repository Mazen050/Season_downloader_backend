from sanic import Sanic
from sanic.response import json,text
from sanic_ext import Extend
from asyncakwam import akwamscrape as ak
from scrapewecima import wecimatitle, wecimaimage, wecimasearch, wecimaseasons
from fasterwecima import wecimascraper
from arabseed_async import arabseed_download, searcharab

app = Sanic("MyHelloWorldApp")
Extend(app)

@app.route('/',methods = ["GET","POST"])
async def index(request):
    if request.method == 'POST':
        data = request.get_json()
        Type = data.get('Type')
        link = data.get('link')
        print(link)
        if Type == "akwam":
            akwam = ak()
            data = akwam.getDLL(link)
        elif Type == "wecima":
            data = wecimascraper(link)
        elif Type == "arabseed":
            data = arabseed_download(link)

        return json(data)
    return text('Hello from Flask!')

@app.route('/search/wecima',methods=['GET','POST'])
async def searchwecima(request):
    if request.method == 'POST':
        data = request.get_json()
        link = data.get('link')
        data = wecimaseasons(link)
        print(data)
        return json(data)
    return text('Hello from Flask!')


@app.route('/search',methods=['GET','POST'])
async def search(request):
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text')
        type = data.get('Type')
        print(text)
        if type=="akwam":
            akwam = ak()
            data = akwam.akwamsearch(text)
        elif type=="wecima":
            data = wecimasearch(text)
        elif type=="arabseed":
            data = searcharab(text)
        print(data)
        return json(data)
    return text('Hello from Flask!')

