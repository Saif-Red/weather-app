from weather_api import get_coordinates, get_weather

city = input("Enter city: ")
city = city.strip()
if not city:
    print("Please enter a city name.")
    exit()
try:
    latitude, longitude, country = get_coordinates(city)
    weather = get_weather(latitude, longitude)

    print("\n7-Day Forecast:")

    for day in weather["forecast"]:
        print(
            day["date"],
            "|",
            day["icon"],
            day["condition"],
            "| High:",
            day["max_temperature"],
            "| Low:",
            day["min_temperature"]
        )

except ValueError as error:
    print(error)
    exit()
except ConnectionError as error:
    print(error)
    exit()
print("Weather for", city, "\n")
print("Temperature:", weather["temperature"], weather["temperature_unit"])
print("Feels like:", weather["feels_like"], weather["feels_like_unit"])
print("Humidity:", weather["humidity"], weather["humidity_unit"])
print("Wind speed:", weather["wind_speed"], weather["wind_speed_unit"])
print("Pressure:", weather["pressure"], weather["pressure_unit"])