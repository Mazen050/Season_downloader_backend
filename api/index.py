from types import MethodType
from flask import Flask, request, jsonify
from flask_cors import CORS
from scrapewecima import wecimascraper, wecimatitle, wecimaimage, wecimasearch, wecimaseasons

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET','POST'])
def index():
   if request.method == 'POST':
       data = request.get_json()
       Type = data.get('Type')
       link = data.get('link')
       print(link)
       if "wecima" in link:
            data = wecimascraper(link)
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
        if type=="wecima":
            data = wecimasearch(text)
        print(data)
        return jsonify(data)
    return 'Hello from Flask!'

if __name__ == '__main__':
  app.run(debug=True,port=5500)
