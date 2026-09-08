import requests

def get_weather_condition(code):
    conditions = {
        0: ("☀️", "Clear sky"),
        1: ("🌤️", "Mainly clear"),
        2: ("⛅", "Partly cloudy"),
        3: ("☁️", "Overcast"),
        45: ("🌫️", "Fog"),
        48: ("🌫️", "Rime fog"),
        51: ("🌦️", "Light drizzle"),
        53: ("🌦️", "Drizzle"),
        55: ("🌧️", "Heavy drizzle"),
        61: ("🌧️", "Light rain"),
        63: ("🌧️", "Rain"),
        65: ("🌧️", "Heavy rain"),
        71: ("🌨️", "Light snow"),
        73: ("🌨️", "Snow"),
        75: ("❄️", "Heavy snow"),
        80: ("🌦️", "Rain showers"),
        81: ("🌧️", "Rain showers"),
        82: ("⛈️", "Heavy rain showers"),
        95: ("⛈️", "Thunderstorm"),
        96: ("⛈️", "Thunderstorm with hail"),
        99: ("⛈️", "Thunderstorm with heavy hail")
    }

    return conditions.get(
        code,
        ("🌡️", "Unknown")
    )

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
    except requests.RequestException as error:
        raise ConnectionError(
            "Unable to connect to the weather service."
        ) from error
    
    data = response.json()
    results = data.get("results")

    if not results:
        raise ValueError(
            "City not found. Please check the spelling and try again."
        )

    location = results[0]
    latitude = location["latitude"]
    longitude = location["longitude"]
    country = location.get("country", "")
    return latitude, longitude, country

def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,pressure_msl,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "forecast_days": 7
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as error:
        print("API Error:", error)
        raise ConnectionError(
            "Unable to retrieve weather information."
        ) from error

    data = response.json()
    current = data["current"]
    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    feels_like = current["apparent_temperature"]
    wind_speed = current["wind_speed_10m"]
    pressure = current["pressure_msl"]

    current_weather_code = current["weather_code"]

    current_icon, current_condition = get_weather_condition(
        current_weather_code
    )

    current_units = data["current_units"]
    temperature_unit = current_units["temperature_2m"]
    humidity_unit = current_units["relative_humidity_2m"]
    feels_like_unit = current_units["apparent_temperature"]
    wind_speed_unit = current_units["wind_speed_10m"]
    pressure_unit = current_units["pressure_msl"]

    daily = data["daily"]

    forecast = []

    for i in range(7):
        icon, condition = get_weather_condition(
            daily["weather_code"][i]
        )

        forecast.append({
            "date": daily["time"][i],
            "weather_code": daily["weather_code"][i],
            "icon": icon,
            "condition": condition,
            "max_temperature": daily["temperature_2m_max"][i],
            "min_temperature": daily["temperature_2m_min"][i]
        })

    weather = {
        "temperature" : temperature,
        "feels_like" : feels_like,
        "humidity" : humidity,
        "wind_speed" : wind_speed,
        "pressure" : pressure,

        "current_weather_code": current_weather_code,
        "current_icon": current_icon,
        "current_condition": current_condition,

        "temperature_unit" : temperature_unit,
        "humidity_unit" : humidity_unit,
        "feels_like_unit" : feels_like_unit,
        "wind_speed_unit" : wind_speed_unit,
        "pressure_unit" : pressure_unit,

        "forecast" : forecast
    }
    return weather