import requests
import os
import time

def fetch_weather_data(cities):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    weather_data = []
    
    for city in cities:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            response = requests.get(url)
            response.raise_for_status()  # Lève une erreur pour les codes d'échec HTTP
            data = response.json()
            weather_data.append(data)
            time.sleep(1)  # Respecter la limite d'appels API
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des données pour {city}: {e}")
    
    return weather_data
