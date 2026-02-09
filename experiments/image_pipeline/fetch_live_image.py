import requests
from pathlib import Path

# Lohegaon coordinates
LAT = 18.5793
LON = 73.9089

# Output path
OUTPUT_DIR = Path("../../data/images/live")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "live_cloud.png"

# Open-Meteo static map (cloud layer)
IMAGE_URL = (
    f"https://maps.open-meteo.com/weather?"
    f"latitude={LAT}&longitude={LON}&zoom=7&layer=clouds"
)

print("🌐 Fetching live cloud image...")

try:
    response = requests.get(IMAGE_URL, timeout=15)
    response.raise_for_status()

    with open(OUTPUT_FILE, "wb") as f:
        f.write(response.content)

    print(f"✅ Live image saved at: {OUTPUT_FILE}")

except Exception as e:
    print("❌ Failed to fetch image")
    print("Reason:", e)