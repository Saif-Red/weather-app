import customtkinter as ctk
from datetime import datetime
import threading
from weather_api import get_coordinates, get_weather

# =========================
# Application Configuration
# =========================

APP_TITLE = "Weather App"
APP_WIDTH = 1100
APP_HEIGHT = 800

# =========================
# Theme
# =========================

BG_COLOR = "#F4F7FB"
CARD_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#2563EB"
TEXT_COLOR = "#172033"
SECONDARY_TEXT = "#64748B"

# =========================
# Main Window
# =========================

app = ctk.CTk()

app.title(APP_TITLE)
app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
app.minsize(900, 600)

app.configure(fg_color=BG_COLOR)

# =========================
# Main Content
# =========================

content_frame =ctk.CTkFrame(
    app,
    fg_color = BG_COLOR,
    corner_radius = 0
)

content_frame.pack(
    fill = "both",
    expand = True
)

# =========================
# Header
# =========================

header_frame = ctk.CTkFrame(
    content_frame,
    fg_color = BG_COLOR,
    corner_radius = 0
)

header_frame.pack(
    fill = "x",
    padx = 40,
    pady = (20,15)
)

app_name = ctk.CTkLabel(
    header_frame,
    text = "Weather",
    font = ("Segoe UI", 24, "bold"),
    text_color = TEXT_COLOR
)

app_name.pack(side="left")

def update_clock():
    current_time = datetime.now().strftime("%H:%M:%S")
    clock_label.configure(text=current_time)

    app.after(1000, update_clock)

# =========================
# Menu Content
# =========================

menu_button = ctk.CTkButton(
    header_frame,
    text = "☰",
    width = 40,
    height = 40,
    fg_color = BG_COLOR,
    hover_color = "#E8EDF5",
    text_color = TEXT_COLOR,
    font = ("Segoe UI", 20),
    corner_radius = 10
)

menu_button.pack(side="right")

menu_frame = ctk.CTkFrame(
    app,
    width = 150,
    height = 130,
    fg_color = CARD_COLOR,
    corner_radius = 12,
    border_width = 1,
    border_color = "#D8E0EB"
)

menu_frame.pack_propagate(False)

help_button = ctk.CTkButton(
    menu_frame,
    text = "Help",
    height = 35,
    fg_color = CARD_COLOR,
    hover_color = "#E8EDF5",
    text_color = TEXT_COLOR,
    anchor = "w",
    corner_radius = 8
)

help_button.pack(
    fill = "x",
    padx = 8,
    pady = (8,2)
)

about_button = ctk.CTkButton(
    menu_frame,
    text = "About",
    height = 35,
    fg_color = CARD_COLOR,
    hover_color = "#E8EDF5",
    text_color = TEXT_COLOR,
    anchor = "w",
    corner_radius = 8
)

about_button.pack(
    fill = "x",
    padx = 8,
    pady = 2
)

settings_button = ctk.CTkButton(
    menu_frame,
    text = "Settings",
    height = 35,
    fg_color = CARD_COLOR,
    hover_color = "#E8EDF5",
    text_color = TEXT_COLOR,
    anchor = "w",
    corner_radius = 8
)

settings_button.pack(
    fill = "x",
    padx = 8,
    pady = 2
)

menu_frame.place_forget()

def toggle_menu():

    print("MENU BUTTON CLICKED")

    if menu_frame.winfo_ismapped():
        menu_frame.place_forget()
        return

    menu_frame.place(
        relx = 1.0,
        rely = 0.0,
        anchor = "ne",
        x = -25,
        y = 90
    )

    menu_frame.lift()

menu_button.configure(
    command = toggle_menu
)

clock_label = ctk.CTkLabel(
    header_frame,
    text = "00:00:00",
    font = ("Segoe UI", 12),
    text_color = SECONDARY_TEXT
)

clock_label.pack(side="right", padx=(0, 15))

# =========================
# Scorllable Content
# =========================

scroll_frame = ctk.CTkScrollableFrame(
    content_frame,
    fg_color = BG_COLOR,
    corner_radius = 0
)

scroll_frame.pack(
    fill = "both",
    expand = True,
    padx = 25,
    pady = (0, 10)
)

# =========================
# Search Section
# =========================

search_frame = ctk.CTkFrame(
    scroll_frame,
    fg_color = BG_COLOR,
    corner_radius = 0
)

search_frame.pack(
    fill = "x",
    pady = (0, 30)
)

city_entry = ctk.CTkEntry(
    search_frame,
    placeholder_text = "Search for a city...",
    height = 50,
    font = ("Segoe UI", 14),
    text_color = TEXT_COLOR,
    placeholder_text_color = SECONDARY_TEXT,
    fg_color = CARD_COLOR,
    border_color = "#D8E0EB",
    corner_radius = 12
)

city_entry.pack(
    side = "left",
    fill = "x",
    expand = True,
    padx = (0, 12)
)

def select_search_text(event=None):
    city_entry.focus_set()
    city_entry.select_range(0, "end")

city_entry.bind(
    "<Button-1>",
    select_search_text
)

city_entry.bind(
    "<Return>",
    lambda event: search_weather()
)

# =========================
# Weather Search Functions
# =========================

def show_error(message, city):
    search_button.configure(
        state = "normal",
        text = "Search"
    )

    if "City not found" in message:
        error_window = ctk.CTkToplevel(app)

        error_window.title("City Not Found")
        error_window.geometry("400x220")
        error_window.resizable(False, False)

        error_window.transient(app)
        error_window.grab_set()

        title_label = ctk.CTkLabel(
            error_window,
            text = "⚠️ City Not Found",
            font = ("Segoe UI", 20, "bold"),
            text_color = TEXT_COLOR
        )

        title_label.pack(
            pady=(30, 10)
        )

        message_label = ctk.CTkLabel(
            error_window,
            text = (
                f'We couldn\'t find weather information for\n'
                f'"{city}".\n\n'
                f'Please check the city name and try again.'
            ),
            font = ("Segoe UI", 13),
            text_color = SECONDARY_TEXT,
            justify = "center"
        )

        message_label.pack(
            pady=(0,20)
        )

        ok_button = ctk.CTkButton(
            error_window,
            text = "OK",
            width = 100,
            height = 35,
            fg_color = PRIMARY_COLOR,
            hover_color = "#1D4ED8",
            command = error_window.destroy
        )

        ok_button.pack()

        error_window.bind(
            "<Return>",
            lambda event: ok_button.invoke()
        )

        error_window.focus_force()

    else:
        error_window = ctk.CTkToplevel(app)

        error_window.title("Weather Error")
        error_window.geometry("400x200")
        error_window.resizable(False, False)

        error_window.transient(app)
        error_window.grab_set()

        title_label = ctk.CTkLabel(
            error_window,
            text = "⚠️ Something went wrong",
            font = ("Segoe UI", 20, "bold"),
            text_color = TEXT_COLOR
        )

        title_label.pack(
            pady=(30,10)
        )

        message_label = ctk.CTkLabel(
            error_window,
            text = message,
            font = ("Segoe UI", 13),
            text_color = SECONDARY_TEXT,
            justify = "center"
        )

        message_label.pack(
            pady = (0, 20)
        )

        ok_button = ctk.CTkButton(
            error_window,
            text = "OK",
            width = 100,
            height = 35,
            fg_color = PRIMARY_COLOR,
            hover_color = "#1D4ED8",
            command = error_window.destroy
        )

        error_window.bind(
            "<Return>",
            lambda event: ok_button.invoke()
        )

        ok_button.pack()

        error_window.focus_force()

def fetch_weather(city):
    try:
        latitude, longitude, country = get_coordinates(city)
        weather = get_weather(latitude, longitude)

    except ValueError as error:
        message = str(error)
        app.after(
            0,
            lambda: show_error(
                message,
                city
            )
        )
        return

    except ConnectionError as error:
        message = str(error)
        app.after(
            0,
            lambda: show_error(
                message,
                city
            )
        )
        return

    app.after(
        0,
        lambda: update_weather_display(
            city,
            country,
            weather
        )
    )

def update_weather_display(city, country, weather):

    location_label.configure(
        text = f"{city.title()}, {country}"
    )    
        
    weather_icon.configure(
        text = weather["current_icon"]
    )
        
    temperature_label.configure(
        text = f'{weather["temperature"]}{weather["temperature_unit"]}'
    )
        
    condition_label.configure(
        text = weather["current_condition"]
    )
        
    feels_like_label.configure(
        text = (
            f'Feels like '
            f'{weather["feels_like"]}'
            f'{weather["feels_like_unit"]}'
        )
    )
        
    humidity_value.configure(
        text = (
            f'{weather["humidity"]} '
            f'{weather["humidity_unit"]}'
        )
    )
        
    wind_value.configure(
        text = (
            f'{weather["wind_speed"]} '
            f'{weather["wind_speed_unit"]}'
        )
    )
        
    pressure_value.configure(
        text = (
            f'{weather["pressure"]} '
            f'{weather["pressure_unit"]}'
        )
    )
        
    update_forecast(
        weather["forecast"]
    )

    updated_label.configure(
        text = "Current weather"
    )

    search_button.configure(
        state = "normal",
        text = "Search"
    )

def search_weather():
    city = city_entry.get().strip()

    if not city:
        print("Please enter a city name.")
        return

    search_button.configure(
        state = "disabled",
        text = "Loading..."
    )

    updated_label.configure(
        text = "Fetching weather data..."
    )

    threading.Thread(
        target = fetch_weather,
        args = (city,),
        daemon = True
    ).start()

search_button = ctk.CTkButton(
    search_frame,
    text = "Search",
    width = 120,
    height = 50,
    font = ("Segoe UI", 13, "bold"),
    fg_color = PRIMARY_COLOR,
    hover_color = "#1D4ED8",
    text_color = "white",
    corner_radius = 12,
    command = search_weather
)

search_button.pack(side="right")



# =========================
# Current Weather Section
# =========================

weather_card = ctk.CTkFrame(
    scroll_frame,
    fg_color = CARD_COLOR,
    corner_radius = 24
)

weather_card.pack(
    fill = "x",
    pady = (0, 25)
)

location_label = ctk.CTkLabel(
    weather_card,
    text = "Tokyo, Japan",
    font = ("Segoe UI", 24, "bold"),
    text_color = TEXT_COLOR
)

location_label.pack(
    pady = (30, 0)
)

updated_label = ctk.CTkLabel(
    weather_card,
    text = "Current weather",
    font = ("Segoe UI", 12),
    text_color = SECONDARY_TEXT
)

updated_label.pack(
    pady = (4, 15)
)

weather_icon = ctk.CTkLabel(
    weather_card,
    text = "☀",
    font = ("Segoe UI", 64),
    text_color = TEXT_COLOR
)

weather_icon.pack(
    pady = (0, 5)
)

temperature_label = ctk.CTkLabel(
    weather_card,
    text = "26.1°C",
    font = ("Segoe UI", 52, "bold"),
    text_color = TEXT_COLOR
)

temperature_label.pack(
    pady = (0, 0)
)

condition_label = ctk.CTkLabel(
    weather_card,
    text = "Clear sky",
    font = ("Segoe UI", 13),
    text_color = SECONDARY_TEXT
)

condition_label.pack(
    pady = (0, 25)
)

feels_like_label = ctk.CTkLabel(
    weather_card,
    text = "Feels like 29.9°C",
    font = ("Segoe UI", 14),
    text_color = SECONDARY_TEXT
)

feels_like_label.pack(
    pady = (5, 30)
)

# =========================
# Weather Details
# =========================

details_frame = ctk.CTkFrame(
    scroll_frame,
    fg_color = BG_COLOR,
    corner_radius = 0
)

details_frame.pack(
    fill = "x",
    pady = (0, 25)
)

details_frame.grid_columnconfigure(
    0,
    weight = 1
)

details_frame.grid_columnconfigure(
    1,
    weight = 1
)

details_frame.grid_columnconfigure(
    2,
    weight = 1
)

humidity_card = ctk.CTkFrame(
    details_frame,
    fg_color = CARD_COLOR,
    corner_radius = 18
)

humidity_card.grid(
    row = 0,
    column = 0,
    padx = (0, 0),
    sticky  = "nsew"
)

humidity_icon = ctk.CTkLabel(
    humidity_card,
    text = "💧",
    font = ("Segoe UI Emoji", 26)
)

humidity_icon.pack(
    pady = (18, 5)
)

humidity_title = ctk.CTkLabel(
    humidity_card,
    text = "HUMIDITY",
    font = ("Segoe UI", 11, "bold"),
    text_color = SECONDARY_TEXT
)

humidity_title.pack()

humidity_value = ctk.CTkLabel(
    humidity_card,
    text = " 72 %",
    font = ("Segoe UI", 20, "bold"),
    text_color = TEXT_COLOR
)

humidity_value.pack(
    pady = (5, 18)
)

# WIND

wind_card = ctk.CTkFrame(
    details_frame,
    fg_color = CARD_COLOR,
    corner_radius = 18
)

wind_card.grid(
    row = 0,
    column = 1,
    padx = 8,
    sticky = "nsew"
)

wind_icon = ctk.CTkLabel(
    wind_card,
    text = "💨",
    font = ("Segoe UI Emoji", 26)
)

wind_icon.pack(
    pady = (18, 5)
)

wind_title = ctk.CTkLabel(
    wind_card,
    text = "WIND",
    font = ("Segoe UI", 11, "bold"),
    text_color = SECONDARY_TEXT
)

wind_title.pack()

wind_value = ctk.CTkLabel(
    wind_card,
    text = "2.6 km/h",
    font = ("Segoe UI", 20, "bold"),
    text_color = TEXT_COLOR
)

wind_value.pack(
    pady = (5, 18)
)

# PRESSURE

pressure_card = ctk.CTkFrame(
    details_frame,
    fg_color = CARD_COLOR,
    corner_radius = 18
)

pressure_card.grid(
    row = 0,
    column = 2,
    padx = (8, 0),
    sticky = "nsew"
)

pressure_icon = ctk.CTkLabel(
    pressure_card,
    text = "◉",
    font = ("Segoe UI", 26),
    text_color = TEXT_COLOR
)

pressure_icon.pack(
    pady = (18, 5)
)

pressure_title = ctk.CTkLabel(
    pressure_card,
    text = "PRESSURE",
    font = ("Segoe UI", 11, "bold"),
    text_color = SECONDARY_TEXT
)

pressure_title.pack()

pressure_value = ctk.CTkLabel(
    pressure_card,
    text = "1008.8 hPa",
    font = ("Segoe UI", 20, "bold"),
    text_color = TEXT_COLOR
)

pressure_value.pack(
    pady = (5, 18)
)

# =========================
# 7-Day Forecast
# =========================

forecast_card = ctk.CTkFrame(
    scroll_frame,
    fg_color = CARD_COLOR,
    corner_radius =20
)

forecast_card.pack(
    fill = "x",
    pady = (0, 25)
)

forecast_title = ctk.CTkLabel(
    forecast_card,
    text = "7-Day FORECAST",
    font = ("Segoe UI", 12, "bold"),
    text_color = SECONDARY_TEXT
)

forecast_title.pack(
    anchor = "w",
    padx =25,
    pady = (20, 10)
)

forecast_frame = ctk.CTkFrame(
    forecast_card,
    fg_color = CARD_COLOR
)

forecast_frame.pack(
    fill = "x",
    padx = 20,
    pady = (0, 20)
)

for column in range(7):
    forecast_frame.grid_columnconfigure(
        column,
        weight = 1
    )

def create_forecast_day(parent, column):
    day_frame = ctk.CTkFrame(
        parent,
        fg_color = CARD_COLOR
    )

    day_frame.grid(
        row = 0,
        column = column,
        padx = 5,
        sticky = "nsew"
    )

    day_label = ctk.CTkLabel(
        day_frame,
        text = "---",
        font = ("Segoe UI", 11, "bold"),
        text_color = SECONDARY_TEXT
    )

    day_label.pack(
        pady = (5, 8)
    )

    icon_label = ctk.CTkLabel(
        day_frame,
        text = "🌡️",
        font = ("Segoe UI Emoji", 28)
    )

    icon_label.pack(
        pady = 5
    )

    temperature_label = ctk.CTkLabel(
        day_frame,
        text = "--° / --°",
        font = ("Segoe UI", 12, "bold"),
        text_color = TEXT_COLOR
    )

    temperature_label.pack(
        pady = (5, 10)
    )

    return {
        "day": day_label,
        "icon": icon_label,
        "temperature": temperature_label
    }

forecast_widgets = []

for column in range(7):
    widgets = create_forecast_day(
        forecast_frame,
        column
    )

    forecast_widgets.append(widgets)

def update_forecast(forecast):
    for index, day_data in enumerate(forecast):
        date = datetime.strptime(
            day_data["date"],
            "%Y-%m-%d"
        )

        day_name = date.strftime("%a").upper()

        forecast_widgets[index]["day"].configure(
            text = day_name
        )

        forecast_widgets[index]["icon"].configure(
            text = day_data["icon"]
        )

        forecast_widgets[index]["temperature"].configure(
            text = (
                f'{day_data["max_temperature"]:.0f}° / '
                f'{day_data["min_temperature"]:.0f}°'
            )
        )

# =========================
# Start Application
# =========================

update_clock()
app.mainloop()