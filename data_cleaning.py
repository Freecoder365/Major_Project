# data_cleaning.py

import pandas as pd
from config import HISTORICAL_CSV, PROCESSED_CSV

# Load historical data
df = pd.read_csv(HISTORICAL_CSV, parse_dates=['time'])
print(f"Initial data shape: {df.shape}")

# ---------------------------
# Step 1: Handle missing values
# ---------------------------
# Fill missing numeric values with previous value (forward fill)
numeric_cols = ['temp', 'dwpt', 'rhum', 'prcp', 'wdir', 'wspd', 'wpgt', 'pres']
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(method='ffill').fillna(method='bfill')

# Drop columns that are mostly empty or not useful
drop_cols = ['snow', 'tsun', 'coco']
df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)

# ---------------------------
# Step 2: Create time-based features
# ---------------------------
df['hour'] = df['time'].dt.hour
df['day_of_week'] = df['time'].dt.dayofweek
df['month'] = df['time'].dt.month

# ---------------------------
# Step 3: Create lag features (previous hour values)
# ---------------------------
lag_features = ['temp', 'rhum', 'prcp', 'wspd', 'pres']
for col in lag_features:
    df[f'{col}_lag1'] = df[col].shift(1)

# ---------------------------
# Step 4: Create rolling averages (last 3 hours)
# ---------------------------
for col in lag_features:
    df[f'{col}_roll3'] = df[col].rolling(window=3).mean()

# Drop rows with NaNs introduced by shift/rolling
df.dropna(inplace=True)
print(f"Processed data shape: {df.shape}")

# ---------------------------
# Step 5: Save processed CSV
# ---------------------------
df.to_csv(PROCESSED_CSV, index=False)
print(f"✅ Processed data saved at: {PROCESSED_CSV}")
