# experiments/extract_image_features.py
import cv2
import numpy as np
import pandas as pd
import os
import glob

IMAGE_DIR = os.path.join("..","data","images")   # ../data/images
OUTPUT_FILE = os.path.join("..","data","image_features.csv")  # ../data/image_features.csv

os.makedirs(IMAGE_DIR, exist_ok=True)

def extract_image_features(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None, None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = float(np.mean(gray))
    # Cloud density: fraction of bright pixels (threshold 200)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    cloud_density = float(np.sum(thresh == 255) / thresh.size)
    return brightness, cloud_density

def main():
    image_paths = sorted(glob.glob(os.path.join(IMAGE_DIR, "*.jpg")) + glob.glob(os.path.join(IMAGE_DIR, "*.png")))
    rows = []
    for p in image_paths:
        b, c = extract_image_features(p)
        if b is not None:
            rows.append({"image": os.path.basename(p), "brightness": b, "cloud_density": c})
    if rows:
        df = pd.DataFrame(rows)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Saved {len(df)} image feature rows to {OUTPUT_FILE}")
    else:
        print("⚠️ No images found in", IMAGE_DIR, " — add images then rerun.")

if __name__ == "__main__":
    main()
