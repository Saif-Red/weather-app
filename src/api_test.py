import requests

url = "https://geocoding-api.open-meteo.com/v1/search"

params = {
    "name": "New Delhi",
    "count": 1,
    "language": "en",
    "format": "json"
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)
print("Response:")
print(response.json())