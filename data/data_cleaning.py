import pandas as pd

from config import HISTORICAL_CSV, PROCESSED_CSV

print("🔹 Loading historical data...")
df = pd.read_csv(HISTORICAL_CSV)

# Convert time column
df["time"] = pd.to_datetime(df["time"])

# Sort by time (VERY IMPORTANT for time-series)
df = df.sort_values("time")

print(f"Initial shape: {df.shape}")

# ===============================
# Feature Engineering
# ===============================

lag_cols = ["temp", "rhum", "prcp", "wspd", "pres"]

# Create lag features
for col in lag_cols:
    df[f"{col}_lag1"] = df[col].shift(1)

# Create rolling features (safe rolling)
for col in lag_cols:
    df[f"{col}_roll3"] = df[col].rolling(window=3, min_periods=1).mean()

print("Features created.")

# ===============================
# Cleaning Strategy (FIX)
# ===============================

# Drop rows ONLY if core weather values are missing
df.dropna(
    subset=["temp", "rhum", "prcp", "wspd", "pres"],
    inplace=True
)

# Fill remaining NaNs caused by lag/rolling
df.fillna(method="bfill", inplace=True)
df.fillna(method="ffill", inplace=True)

print(f"Final shape after cleaning: {df.shape}")

# ===============================
# Save processed data
# ===============================

df.to_csv(PROCESSED_CSV, index=False)
print("✅ processed.csv saved successfully")
