from types import MethodType
from flask import Flask, request, jsonify
from flask_cors import CORS
from asyncakwam import akwamscrape as ak
#import asyncplaywright as egy
from scrapewecima import wecimatitle, wecimaimage, wecimasearch, wecimaseasons
from fasterwecima import wecimascraper
from arabseed_async import arabseed_download, searcharab
# from egydead import egydead_download

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET','POST'])
def index():
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

       return jsonify(data)
   return 'Hello from Flask!'

@app.route('/search/wecima',methods=['GET','POST'])
def searchwecima():
    if request.method == 'POST':
        data = request.get_json()
        link = data.get('link')
        data = wecimaseasons(link)
        print(data)
        return jsonify(data)
    return 'Hello from Flask!'


@app.route('/search',methods=['GET','POST'])
def search():
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
        return jsonify(data)
    return 'Hello from Flask!'

if __name__ == '__main__':
  app.run(debug=True,port=5500)
