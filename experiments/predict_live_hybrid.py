# experiments/predict_live_hybrid.py
import os
import pandas as pd
import joblib
from extract_image_features import extract_image_features  # local extractor in experiments/

MODEL_PATH = os.path.join("experiments","models","hybrid_weather_model.pkl")
LIVE_PROC = os.path.join("..","data","live_data_processed.csv")  # created by main process_live_data.py
IMAGE_DIR = os.path.join("..","data","images")
IMAGE_CSV = os.path.join("..","data","image_features.csv")

if not os.path.exists(MODEL_PATH):
    raise SystemExit("Model not found at: " + MODEL_PATH)
if not os.path.exists(LIVE_PROC):
    raise SystemExit("Processed live data not found at: " + LIVE_PROC)

print("🔹 Loading hybrid model...")
model = joblib.load(MODEL_PATH)

print("🔹 Loading processed live data...")
live_df = pd.read_csv(LIVE_PROC)
# ensure single latest row
live_row = live_df.tail(1).reset_index(drop=True)

# Add image features: if image_features.csv exists, use last row; else try to compute from latest image file
if os.path.exists(IMAGE_CSV):
    img_df = pd.read_csv(IMAGE_CSV)
    # use last row (or nearest) as simple approach
    brightness = img_df['brightness'].iloc[-1]
    cloud_density = img_df['cloud_density'].iloc[-1]
else:
    # try compute from a file named "latest.jpg" in data/images
    latest_img = os.path.join(IMAGE_DIR, "latest.jpg")
    if os.path.exists(latest_img):
        brightness, cloud_density = extract_image_features(latest_img)
    else:
        # fallback: set zeros
        brightness, cloud_density = 0.0, 0.0

live_row['brightness'] = brightness
live_row['cloud_density'] = cloud_density

# align columns with training (drop targets and time)
train_df = pd.read_csv(os.path.join("..","data","processed.csv"))
targets = ['temp','rhum','prcp','wspd','pres']
feature_cols = [c for c in train_df.columns if c not in targets + ['time']]
X_live = live_row.reindex(columns=feature_cols).fillna(0)

print("\nUsing live features:")
print(X_live.head())

# predict
pred = model.predict(X_live)[0]
output = dict(zip(targets, [round(float(v),2) for v in pred]))

print("\n✅ Hybrid Predictions:")
for k,v in output.items():
    print(f"{k}: {v}")
