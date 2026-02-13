import pandas as pd
import os

LIVE_DATA_PATH = "../data/live_data_processed.csv"
IMAGE_AGG_PATH = "../data/image_features_live_aggregated.csv"
OUTPUT_PATH = "../data/live_with_images.csv"

if not os.path.exists(LIVE_DATA_PATH):
    raise FileNotFoundError("❌ live_data_processed.csv not found")

if not os.path.exists(IMAGE_AGG_PATH):
    raise FileNotFoundError("❌ image_features_live_aggregated.csv not found")

live_df = pd.read_csv(LIVE_DATA_PATH)
img_df = pd.read_csv(IMAGE_AGG_PATH)

# Add image columns to live row
for col in img_df.columns:
    live_df[col] = img_df.iloc[0][col]

live_df.to_csv(OUTPUT_PATH, index=False)

print("✅ Live weather + image features merged")
print(live_df.head())
