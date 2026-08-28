import requests
city = input("Enter city: ")
city = city.strip()

if not city:
    print("Please enter a city name.")
    exit()

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
print("Weather for", city, "\n")
print("Temperature:", temperature)
print("Feels like:", feels_like)
print("Humidity:", humidity)
print("Wind speed:", wind_speed)
print("Pressure:", pressure)