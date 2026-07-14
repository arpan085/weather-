import requests
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_weather_description(code):
    return WEATHER_CODES.get(code, f"Weather code {code}")


def format_updated_time(value):
    try:
        parsed = datetime.fromisoformat(value)
        return parsed.strftime("%b %d, %Y • %I:%M %p")
    except ValueError:
        return value


def lookup_city_coordinates(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    response = requests.get(
        url,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results") or []
    if not results:
        return None

    location = results[0]
    return {
        "name": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "country": location.get("country", ""),
        "admin1": location.get("admin1", ""),
    }

# -------------------------------
# Weather Fetch Function
# -------------------------------
def get_weather():
    city = city_box.get().strip()
    if not city:
        messagebox.showerror("Error", "Please select or enter a city")
        return

    try:
        status_label.config(text=f"Looking up {city}...")
        win.update_idletasks()

        location = lookup_city_coordinates(city)
        if not location:
            messagebox.showerror("Error", f"No location found for '{city}'")
            status_label.config(text="Choose a valid city and try again.")
            return

        # Open-Meteo API (free, no key required)
        url = "https://api.open-meteo.com/v1/forecast"
        response = requests.get(
            url,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current_weather": "true",
                "timezone": "auto",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if "current_weather" not in data:
            messagebox.showerror("Error", "Weather data not available")
            status_label.config(text="Weather data is currently unavailable.")
            return

        weather = data["current_weather"]
        weather_city = location["name"]
        if location["admin1"]:
            weather_city = f"{weather_city}, {location['admin1']}"
        if location["country"]:
            weather_city = f"{weather_city}, {location['country']}"

        # Update labels
        location_label.config(text=f"{weather_city}")
        temp_label.config(text=f"🌡 Temperature: {weather['temperature']}°C")
        wind_label.config(text=f"🌬 Wind speed: {weather['windspeed']} km/h")
        cond_label.config(text=f"☁ Condition: {get_weather_description(weather['weathercode'])}")
        time_label.config(text=f"🕒 Updated at: {format_updated_time(weather['time'])}")
        status_label.config(text="Weather refreshed successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather: {e}")
        status_label.config(text="Could not refresh weather right now.")


# -------------------------------
# Tkinter UI
# -------------------------------
win = tk.Tk()
win.title("Weather App")
win.geometry("560x680")
win.resizable(False, False)
win.configure(bg="#EAF4FF")

style = ttk.Style(win)
style.theme_use("clam")
style.configure(
    "Weather.TCombobox",
    padding=8,
    relief="flat",
)

# Icon (use .ico file)
try:
    win.iconbitmap(r"image\weather.ico")
except:
    pass  # ignore if icon not found

# Title
title = tk.Label(
    win,
    text="🌤 WEATHER APP",
    bg="#EAF4FF",
    fg="#1E293B",
    font=("Segoe UI", 30, "bold")
)
title.pack(pady=20)

subtitle = tk.Label(
    win,
    text="Search any city and get live conditions in seconds.",
    bg="#EAF4FF",
    fg="#475569",
    font=("Segoe UI", 11)
)
subtitle.pack(pady=(0, 16))

# City Combobox
list_name = ["Kathmandu", "Pokhara", "Biratnagar", "Chitwan", "Lalitpur"]
city_box = ttk.Combobox(
    win,
    values=list_name,
    font=("Segoe UI", 14),
    width=28,
    style="Weather.TCombobox"
)
city_box.set("Select City")
city_box.pack(pady=10)
city_box.bind("<Return>", lambda event: get_weather())

# Get Weather Button
done_button = tk.Button(
    win,
    text="Get Weather",
    bg="#4A90E2",
    fg="white",
    activebackground="#357ABD",
    activeforeground="white",
    relief="flat",
    font=("Segoe UI", 12, "bold"),
    cursor="hand2",
    command=get_weather
)
done_button.pack(pady=15)

# Frame for Weather Info
frame = tk.Frame(
    win,
    bg="white",
    bd=0,
    highlightthickness=0,
    relief="flat"
)
frame.place(x=30, y=260, width=500, height=250)

location_label = tk.Label(
    frame,
    text="Weather details will appear here",
    bg="white",
    fg="#0F172A",
    font=("Segoe UI", 16, "bold")
)
location_label.pack(anchor="w", pady=(18, 10), padx=20)

temp_label = tk.Label(frame, text="🌡 Temperature: --°C", bg="white", fg="#1E293B", font=("Segoe UI", 14))
temp_label.pack(anchor="w", pady=5, padx=20)

cond_label = tk.Label(frame, text="☁ Condition: --", bg="white", fg="#1E293B", font=("Segoe UI", 14))
cond_label.pack(anchor="w", pady=5, padx=20)

wind_label = tk.Label(frame, text="🌬 Wind speed: -- km/h", bg="white", fg="#1E293B", font=("Segoe UI", 14))
wind_label.pack(anchor="w", pady=5, padx=20)

time_label = tk.Label(frame, text="🕒 Updated at: --", bg="white", fg="#1E293B", font=("Segoe UI", 14))
time_label.pack(anchor="w", pady=5, padx=20)

status_label = tk.Label(
    win,
    text="Choose a city to see the current weather.",
    bg="#EAF4FF",
    fg="#334155",
    font=("Segoe UI", 10)
)
status_label.pack(pady=(8, 0))

# Footer
footer = tk.Label(
    win,
    text="Made with Python • Arpan085",
    bg="#EAF4FF",
    fg="gray",
    font=("Segoe UI", 9)
)
footer.pack(side=tk.BOTTOM, pady=10)

win.mainloop()
