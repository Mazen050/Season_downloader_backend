from types import MethodType
from flask import Flask, request, jsonify
from flask_cors import CORS
from asyncakwam import akwamscrape as ak
#import asyncplaywright as egy
from scrapewecima import wecimascraper, wecimatitle, wecimaimage
from selenium1 import egydead_download

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET','POST'])
#def index():
#    if request.method == 'POST':
#        data = request.get_json()
#        Type = data.get('Type')
#        link = data.get('link')
#        print(link)
#        if "ak.sv" in link:
#            akwam = ak()
#            data = akwam.getDLL(link)
#        elif "wecima" in link:
#            data = wecimascraper(link)
#        elif "egyrbyeteuh" or "egydead" in link:
#            data = egydead_download(link)
#        return jsonify(data)
#    return 'Hello from Flask!'

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text')
        print(text)
        #if "ak.sv" in text:
        akwam = ak()
        data = akwam.akwamsearch(text)
        #elif "wecima" in text:
        #    data = wecimasearch(text)
        print(data)
        return jsonify(data)
    return 'Hello from Flask!'

if __name__ == '__main__':
  app.run(debug=True,port=5500)
