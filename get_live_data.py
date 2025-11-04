# get_live_data.py

import requests
import json
from datetime import datetime
from config import LAT, LON, LIVE_JSON

url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"

print("Fetching live weather data from Open-Meteo...")

response = requests.get(url)
data = response.json()

# Add timestamp
data["fetched_at"] = datetime.now().isoformat()

# Save to file
with open(LIVE_JSON, "w") as f:
    json.dump(data, f, indent=4)

print(f"✅ Live data saved at: {LIVE_JSON}")
print(json.dumps(data, indent=2))
