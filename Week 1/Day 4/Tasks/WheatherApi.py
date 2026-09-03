import requests

def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()   # raises an error if status isn't 200

        data = response.json()
        weather = data["current_weather"]

        print(f"Temperature: {weather['temperature']}°C")
        print(f"Wind Speed: {weather['windspeed']} km/h")
        print(f"Time: {weather['time']}")

    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)


get_weather(35.9221, 74.3087)