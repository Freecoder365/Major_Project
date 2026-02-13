import pandas as pd
import os

# Paths
IMAGE_FEATURES_PATH = "../../data/image_features_live.csv"
OUTPUT_PATH = "../../data/image_features_live_aggregated.csv"

if not os.path.exists(IMAGE_FEATURES_PATH):
    raise FileNotFoundError("❌ image_features_live.csv not found")

df = pd.read_csv(IMAGE_FEATURES_PATH)

if df.empty:
    raise ValueError("❌ No image data found")

# Aggregate features (mean of all live images)
aggregated = pd.DataFrame([{
    "img_brightness": df["img_brightness"].mean(),
    "img_cloud_density": df["img_cloud_density"].mean()
}])

aggregated.to_csv(OUTPUT_PATH, index=False)

print("✅ Aggregated live image features created")
print(aggregated)
print(f"📁 Saved to: {os.path.abspath(OUTPUT_PATH)}")
