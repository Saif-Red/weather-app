import requests



def get_coordinates(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException:
        print("Unable to connect to the weather service.")
        exit()

    data = response.json()
    results = data.get("results")

    if not results:
        print("City not found. Please check the spelling and try again.")
        exit()

    location = results[0]
    latitude = location["latitude"]
    longitude = location["longitude"]
    return latitude, longitude

def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,pressure_msl"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException:
        print("Unable to retrieve weather information.")
        exit()

    data = response.json()
    current = data["current"]
    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    feels_like = current["apparent_temperature"]
    wind_speed = current["wind_speed_10m"]
    pressure = current["pressure_msl"]

    current_units = data["current_units"]
    temperature_unit = current_units["temperature_2m"]
    humidity_unit = current_units["relative_humidity_2m"]
    feels_like_unit = current_units["apparent_temperature"]
    wind_speed_unit = current_units["wind_speed_10m"]
    pressure_unit = current_units["pressure_msl"]

    weather = {
        "temperature" : temperature,
        "feels_like" : feels_like,
        "humidity" : humidity,
        "wind_speed" : wind_speed,
        "pressure" : pressure,
        "temperature_unit" : temperature_unit,
        "humidity_unit" : humidity_unit,
        "feels_like_unit" : feels_like_unit,
        "wind_speed_unit" : wind_speed_unit,
        "pressure_unit" : pressure_unit
    }
    return weather