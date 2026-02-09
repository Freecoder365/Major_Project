import cv2
import os
import pandas as pd
import numpy as np

# --------------------------------------------------
# Absolute path handling (NO relative confusion)
# --------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
IMAGE_DIR = os.path.join(PROJECT_ROOT, "data/images")
OUTPUT_CSV = os.path.join(PROJECT_ROOT, "data/image_features_live.csv")

print(f"📂 Image directory: {IMAGE_DIR}")

if not os.path.exists(IMAGE_DIR):
    raise FileNotFoundError("❌ data/images directory not found")

image_files = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

if len(image_files) == 0:
    raise RuntimeError("❌ No images found in data/images")

features = []

# --------------------------------------------------
# Process ALL images
# --------------------------------------------------
for img_name in image_files:
    img_path = os.path.join(IMAGE_DIR, img_name)
    img = cv2.imread(img_path)

    if img is None:
        print(f"⚠️ Skipping unreadable image: {img_name}")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Brightness
    brightness = np.mean(gray)

    # Cloud density (simple threshold method)
    cloud_pixels = np.sum(gray > 200)
    cloud_density = cloud_pixels / gray.size

    features.append({
        "image_name": img_name,
        "img_brightness": round(float(brightness), 2),
        "img_cloud_density": round(float(cloud_density), 4)
    })

# --------------------------------------------------
# Save results
# --------------------------------------------------
df = pd.DataFrame(features)
df.to_csv(OUTPUT_CSV, index=False)

print("✅ Live image features extracted for ALL images")
print(df)
print(f"📁 Saved to: {OUTPUT_CSV}")
