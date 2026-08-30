import customtkinter as ctk
from datetime import datetime

# =========================
# Application Configuration
# =========================

APP_TITLE = "Weather App"
APP_WIDTH = 1100
APP_HEIGHT = 750

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
app.minsize(960, 650)

app.configure(fg_color=BG_COLOR)

# =========================
# Main Content
# =========================

main_frame =ctk.CTkFrame(
    app,
    fg_color = BG_COLOR,
    corner_radius = 0
)

main_frame.pack(
    fill = "both",
    expand = True,
    padx = 40,
    pady = 30
)

# =========================
# Header
# =========================

header_frame = ctk.CTkFrame(
    main_frame,
    fg_color = BG_COLOR,
    corner_radius = 0
)

header_frame.pack(
    fill = "x",
    pady = (0,25)
)

app_name = ctk.CTkLabel(
    header_frame,
    text = "Weather",
    font = ("Segoe UI", 24, "bold"),
    text_color = TEXT_COLOR
)

app_name.pack(side="left")

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

clock_label = ctk.CTkLabel(
    header_frame,
    text = "00:00:00",
    font = ("Segoe UI", 12),
    text_color = SECONDARY_TEXT
)

clock_label.pack(side="right", padx=(0, 15))

def update_clock():
    current_time = datetime.now().strftime("%H:%M:%S")
    clock_label.configure(text=current_time)

    app.after(1000, update_clock)

# =========================
# Search Section
# =========================

search_frame = ctk.CTkFrame(
    main_frame,
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

city_entry.bind(
    "<Return>",
    lambda event: search_weather()
)

def search_weather():
    city = city_entry.get().strip()

    if not city:
        print("Please enter a city name.")
        return

    print("Searching for:", city)

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
    main_frame,
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
# Start Application
# =========================

update_clock()
app.mainloop()