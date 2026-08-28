from weather_api import get_coordinates, get_weather

city = input("Enter city: ")
city = city.strip()
if not city:
    print("Please enter a city name.")
    exit()
latitude, longitude = get_coordinates(city)
weather = get_weather(latitude, longitude)
print("Weather for", city, "\n")
print("Temperature:", weather["temperature"], weather["temperature_unit"])
print("Feels like:", weather["feels_like"], weather["feels_like_unit"])
print("Humidity:", weather["humidity"], weather["humidity_unit"])
print("Wind speed:", weather["wind_speed"], weather["wind_speed_unit"])
print("Pressure:", weather["pressure"], weather["pressure_unit"])