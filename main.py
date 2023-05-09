import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

def fetch_data(*, update: bool = False, json_cache:str, url:str ):
    if update:
        json_data = None
    else:
        try:
            with open(json_cache, 'r') as file:
                json_data = json.load(file)
                print("fetched from local cache")
        except(FileNotFoundError, json.JSONDecodeError) as e:
            print(f'No local cache found... ({e})')
            json_data = None
    if not json_data:
        print("fetching new json data - (creating local cache)")
        json_data = requests.get(url).json()
        with open(json_cache, "w") as file:
            json.dump(json_data, file)

    return json_data     

@app.route('/')
def hello():
    return 'Velkommen til vår cache'

@app.route('/cacheJson')
def serve_cache_json():
    url = "http://localhost:6438/contacts"
    json_cache = 'cache.json'
    data: dict = fetch_data(update=False,
                            json_cache=json_cache,
                            url=url)
    with open(json_cache, 'r') as file:
        data = json.load(file)
        return jsonify(data)
    
@app.route('/cacheVcard')
def serve_cache_vcard():
    url = "http://localhost:6438/contacts/vcard"
    json_cache = 'cacheVcard.json'
    data: dict = fetch_data(update=False,
                            json_cache=json_cache,
                            url=url)
    with open(json_cache, 'r') as file:
        data = json.load(file)
        return jsonify(data)    

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5555)  