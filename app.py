from flask import Flask, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Wczytuje zmienne środowiskowe z pliku .env
load_dotenv()

app = Flask(__name__)

# Pobiera klucz z wczytanych zmiennych
# Zwróci None, jeśli klucz nie zostanie znaleziony w pliku
API_KEY = os.getenv("API_KEY")

@app.route('/')
def index():
    # Serwujemy główny plik HTML
    return render_template('index.html')

@app.route('/api/stops')
def get_stops():
    if not API_KEY:
        return jsonify({"error": "Brak klucza API w konfiguracji serwera."}), 500
#https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id= f2e5503e927d-4ad3-9500-4ab9e55deb59&apikey=tu_podaj_swoj_apikey&type=1 


    url = "https://api.um.warszawa.pl/api/action/busestrams_get"
    params = {
        # "id": "ab75c33d-3a26-4342-b36a-6e5fef0a3ac3",
        "resource_id": "f2e5503e927d-4ad3-9500-4ab9e55deb59",
        "apikey": API_KEY,
        "type": 2
    }
    
    # 1. Poprawka: Używamy metody GET zamiast POST
    response = requests.post(url, params=params)
    
    # 2. Poprawka: Zabezpieczenie przed stronami HTML z błędem
    if response.status_code != 200:
        print(f"Błąd połączenia z API! Kod statusu: {response.status_code}")
        print(f"Odpowiedź serwera (zamiast JSON): {response.text}")
        return jsonify({"error": f"Błąd zewnętrznego serwera ({response.status_code})"}), 500

    # 3. Zabezpieczenie parsowania (na wypadek dziwnych danych z miasta)
    try:
        data = response.json()
    except Exception as e:
        print(f"API nie zwróciło JSON-a! Zwróciło to: {response.text}")
        return jsonify({"error": "Niepoprawny format danych z API"}), 500

    clean_data = []
    # print(data)
    if 'result' in data:
        items = data['result'] 
        
        # if isinstance(items, list):
        for item in items:
            print(item)
            bus = {'szer_geo': item['Lat'], 'dlug_geo': item['Lon']}
            if 'szer_geo' in bus and 'dlug_geo' in bus:
                clean_data.append(bus)

    print(f"Pobrano {len(clean_data)} aut obecnie na trasie z API.")
    return jsonify(clean_data)

if __name__ == '__main__':
    print("Aplikacja startuje na: http://127.0.0.1:5000")
    app.run(debug=True)