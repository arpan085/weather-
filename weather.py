import requests

# Replace with your OpenWeatherMap API key
API_KEY = "YOUR_API_KEY"

CITY = "Balaju,Kathmandu,NP"

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        city = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"].title()
        wind = data["wind"]["speed"]

        print("=" * 40)
        print(f"📍 Location     : {city}, {country}")
        print(f"🌡 Temperature  : {temp}°C")
        print(f"🤗 Feels Like   : {feels_like}°C")
        print(f"☁ Weather      : {weather}")
        print(f"💧 Humidity     : {humidity}%")
        print(f"🌬 Wind Speed   : {wind} m/s")
        print("=" * 40)

    else:
        print("Error:", data.get("message"))

except requests.exceptions.RequestException as e:
    print("Network Error:", e)
