# fetch_live_data.py
import requests
import pandas as pd
from datetime import datetime
from config_live import API_KEY, LAT, LON, LIVE_DATA_CSV
import os

def fetch_live_weather():
    """Fetch live weather data from OpenWeatherMap API"""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        print("❌ Error fetching data:", data)
        return None

    # Extract relevant fields
    record = {
        "time": datetime.utcfromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M:%S"),
        "temp": data["main"]["temp"],
        "rhum": data["main"]["humidity"],
        "prcp": data.get("rain", {}).get("1h", 0.0),  # rainfall in mm (default 0 if none)
        "wspd": data["wind"]["speed"],
        "pres": data["main"]["pressure"]
    }

    print("✅ Live weather data fetched successfully:")
    print(record)

    # Save to CSV
    df_new = pd.DataFrame([record])

    if os.path.exists(LIVE_DATA_CSV):
        df_old = pd.read_csv(LIVE_DATA_CSV)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(LIVE_DATA_CSV, index=False)
    print(f"✅ Saved to {LIVE_DATA_CSV}")

if __name__ == "__main__":
    fetch_live_weather()
