import pandas as pd
from config import HISTORICAL_CSV, PROCESSED_CSV

print("🔹 Loading historical data...")
df = pd.read_csv(HISTORICAL_CSV)

# Parse and sort time
df["time"] = pd.to_datetime(df["time"])
df = df.sort_values("time")

print(f"Initial shape: {df.shape}")

# ==========================
# Drop useless / empty cols
# ==========================
drop_cols = ["snow", "wpgt", "tsun"]
df = df.drop(columns=[c for c in drop_cols if c in df.columns])

# ==========================
# Keep only core parameters
# ==========================
keep_cols = [
    "time", "temp", "dwpt", "rhum", "prcp",
    "wdir", "wspd", "pres"
]
df = df[keep_cols]

# ==========================
# Fill missing values (KEY)
# ==========================
df = df.interpolate(method="linear")
df = df.fillna(method="bfill").fillna(method="ffill")

# ==========================
# Time features
# ==========================
df["hour"] = df["time"].dt.hour
df["day_of_week"] = df["time"].dt.dayofweek
df["month"] = df["time"].dt.month

# ==========================
# Lag features
# ==========================
for col in ["temp", "rhum", "prcp", "wspd", "pres"]:
    df[f"{col}_lag1"] = df[col].shift(1)

# ==========================
# Rolling features
# ==========================
for col in ["temp", "rhum", "prcp", "wspd", "pres"]:
    df[f"{col}_roll3"] = df[col].rolling(3, min_periods=1).mean()

# Final safety fill
df = df.fillna(method="bfill").fillna(method="ffill")

print(f"Final shape after cleaning: {df.shape}")

df.to_csv(PROCESSED_CSV, index=False)
print("✅ processed.csv saved successfully")
