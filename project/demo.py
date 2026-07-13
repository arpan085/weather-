import requests
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# -------------------------------
# Weather Fetch Function
# -------------------------------
def get_weather():
    city = city_box.get()
    if not city:
        messagebox.showerror("Error", "Please select or enter a city")
        return

    try:
        # Open-Meteo API (free, no key required)
        url = f"https://api.open-meteo.com/v1/forecast?latitude=27.7172&longitude=85.3240&current_weather=true"
        # NOTE: Replace lat/long with dynamic lookup if you want multiple cities
        response = requests.get(url)
        data = response.json()

        if "current_weather" not in data:
            messagebox.showerror("Error", "Weather data not available")
            return

        weather = data["current_weather"]

        # Update labels
        temp_label.config(text=f"🌡 Temperature : {weather['temperature']}°C")
        wind_label.config(text=f"🌬 Wind Speed  : {weather['windspeed']} km/h")
        cond_label.config(text=f"☁ Condition   : {weather['weathercode']}")
        time_label.config(text=f"🕒 Updated At : {weather['time']}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather: {e}")


# -------------------------------
# Tkinter UI
# -------------------------------
win = tk.Tk()
win.title("Weather App")
win.geometry("520x620")
win.resizable(False, False)
win.configure(bg="#EAF4FF")

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
    font=("Segoe UI", 28, "bold")
)
title.pack(pady=20)

# City Combobox
list_name = ["Kathmandu", "Pokhara", "Biratnagar", "Chitwan", "Lalitpur"]
city_box = ttk.Combobox(
    win,
    values=list_name,
    font=("Segoe UI", 14),
    width=25
)
city_box.set("Select City")
city_box.pack(pady=10)

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
    highlightthickness=0
)
frame.place(x=20, y=240, width=460, height=220)

temp_label = tk.Label(frame, text="🌡 Temperature : --°C", bg="white", fg="#1E293B", font=("Segoe UI", 14))
temp_label.pack(anchor="w", pady=5, padx=20)

cond_label = tk.Label(frame, text="☁ Condition   : --", bg="white", fg="#1E293B", font=("Segoe UI", 14))
cond_label.pack(anchor="w", pady=5, padx=20)

wind_label = tk.Label(frame, text="🌬 Wind Speed  : -- km/h", bg="white", fg="#1E293B", font=("Segoe UI", 14))
wind_label.pack(anchor="w", pady=5, padx=20)

time_label = tk.Label(frame, text="🕒 Updated At : --", bg="white", fg="#1E293B", font=("Segoe UI", 14))
time_label.pack(anchor="w", pady=5, padx=20)

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
