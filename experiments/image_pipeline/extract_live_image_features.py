import cv2
import numpy as np
import pandas as pd
from pathlib import Path
import os

# ---------------------------
# Configuration
# ---------------------------
IMG_DIR = Path("../../data/images")
OUT_CSV = Path("../../data/image_features_live.csv")

# ---------------------------
# Check image directory
# ---------------------------
if not IMG_DIR.exists():
    print(f"❌ Image directory not found: {IMG_DIR.resolve()}")
    exit()

images = sorted(IMG_DIR.glob("*.jpg"))

if len(images) == 0:
    print("❌ No images found in data/images/")
    exit()

latest_image = images[-1]
print(f"📸 Using image: {latest_image.name}")

# ---------------------------
# Load image safely
# ---------------------------
img = cv2.imread(str(latest_image), cv2.IMREAD_GRAYSCALE)

if img is None:
    print("❌ OpenCV failed to load the image.")
    print("👉 Possible causes: corrupted image or unsupported format")
    exit()

# ---------------------------
# Feature extraction
# ---------------------------
brightness = float(np.mean(img))
cloud_density = float((img < 200).mean())

# ---------------------------
# Save features
# ---------------------------
df = pd.DataFrame([{
    "image_name": latest_image.name,
    "img_brightness": brightness,
    "img_cloud_density": cloud_density
}])

df.to_csv(OUT_CSV, index=False)

print("✅ Live image features extracted successfully")
print(df)
