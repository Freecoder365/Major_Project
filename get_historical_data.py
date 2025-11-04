# get_historical_data.py

from meteostat import Point, Hourly
from datetime import datetime, timedelta
import pandas as pd
from config import LAT, LON, HISTORICAL_CSV

# Define location (Santacruz)
location = Point(LAT, LON)

# Define time period (past 365 days)
end = datetime.now()
start = end - timedelta(days=365)

print(f"Fetching weather data from {start.date()} to {end.date()} for Santacruz...")

# Fetch hourly data from Meteostat
data = Hourly(location, start, end)
data = data.fetch()

# Reset index for clarity
data.reset_index(inplace=True)

# Save to CSV
data.to_csv(HISTORICAL_CSV, index=False)
print(f"✅ Historical data saved at: {HISTORICAL_CSV}")

# Show quick summary
print(data.head())
print(f"\nTotal records fetched: {len(data)}")
