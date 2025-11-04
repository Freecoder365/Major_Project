import pandas as pd
from datetime import datetime

RAW_LIVE_PATH = "data/live_data.csv"
PROCESSED_TRAIN_PATH = "data/processed.csv"
PROCESSED_LIVE_PATH = "data/live_data_processed.csv"

print("🔹 Loading raw live data...")
df_live = pd.read_csv(RAW_LIVE_PATH)
df_train = pd.read_csv(PROCESSED_TRAIN_PATH)

# Take the latest live record
latest = df_live.tail(1).copy()
latest["time"] = pd.to_datetime(latest["time"])

# Basic feature engineering
latest["month"] = latest["time"].dt.month
latest["day_of_week"] = latest["time"].dt.dayofweek
latest["hour"] = latest["time"].dt.hour
latest["dwpt"] = latest["temp"] - ((100 - latest["rhum"]) / 5)

# 🔸 Ensure wspd and wpgt exist
if "wspd" not in latest.columns:
    latest["wspd"] = 0
if "wpgt" not in latest.columns:
    latest["wpgt"] = 0

# 🔸 Fill in expected columns
for col in df_train.columns:
    if col not in latest.columns:
        if "lag" in col or "roll" in col:
            latest[col] = 0
        elif col in ["wdir", "wspd", "wpgt"]:
            latest[col] = 0
        else:
            latest[col] = 0

# 🔸 Keep only columns the model expects
processed = latest[df_train.columns.intersection(latest.columns)]

processed.to_csv(PROCESSED_LIVE_PATH, index=False)
print("✅ Live data processed and aligned with training features.")
print(processed)
