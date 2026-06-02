from flask import Flask, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
import argparse
from extractors import get_busestrams, get_stops#, get_streets


load_dotenv()


parser = argparse.ArgumentParser()
parser.add_argument('-m', default='buses', help='desired mode: buses, trams, stops, streets')
args = parser.parse_args()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

modes = {
    'buses': {'http_method': requests.post,
              'params': {"resource_id": "f2e5503e927d-4ad3-9500-4ab9e55deb59", "type": 1, "apikey": API_KEY}, 
              'endpoint': 'busestrams_get', "data_extractor": get_busestrams},
    'trams': {'http_method': requests.post,
              'params': {"resource_id": "f2e5503e927d-4ad3-9500-4ab9e55deb59", "type": 2, "apikey": API_KEY}, 
              'endpoint': 'busestrams_get', "data_extractor": get_busestrams},
    'stops': {'http_method': requests.get,
                'params': {"id": "ab75c33d-3a26-4342-b36a-6e5fef0a3ac3", "apikey": API_KEY}, 
                'endpoint': 'dbtimetable_get', "data_extractor": get_stops},
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ask')
def get_data():
    if not API_KEY:
        return jsonify({"error": "Brak klucza API w konfiguracji serwera."}), 500
    url = "/".join(["https://api.um.warszawa.pl/api/action", modes[args.m]['endpoint']])
    params = modes[args.m]['params']
    
    response = modes[args.m]['http_method'](url, params=params)
    print(response.url)
    
    # Catch errors from the API
    if response.status_code != 200:
        print(f"Error with API connection! Status code: {response.status_code}")
        print(f"Server response (instead of JSON): {response.text}")
        print(f"URL: {response.url}")
        return jsonify({"error": f"Error from external server ({response.status_code})"}), 500

    # Catch JSON parsing errors
    try:
        data = response.json()
    except Exception as e:
        print(f"API did not return JSON! Response: {response.text}")
        return jsonify({"error": "Improper JSON returned by API"}), 500

    clean_data = jsonify(modes[args.m]['data_extractor'](data))
    return clean_data

if __name__ == '__main__':
    print("Aplikacja startuje na: http://127.0.0.1:5000")
    app.run(debug=True)