# merge_image_features.py
"""
Merges extracted image features with the processed tabular training data.
Place this file into experiments/ and run from experiments/.
"""

import os
import pandas as pd

PROCESSED_CSV = os.path.join("..", "data", "processed.csv")
IMAGE_FEATS_CSV = os.path.join("..", "data", "image_features.csv")
OUT_MERGED = os.path.join("..", "data", "processed_with_images.csv")

print("Loading processed CSV:", PROCESSED_CSV)
df_tab = pd.read_csv(PROCESSED_CSV)

if not os.path.exists(IMAGE_FEATS_CSV):
    raise SystemExit(f"ERROR: image features file not found: {IMAGE_FEATS_CSV}")

print("Loading image features:", IMAGE_FEATS_CSV)
df_img = pd.read_csv(IMAGE_FEATS_CSV)

if 'time' in df_tab.columns and 'time' in df_img.columns:
    print("Both tables have 'time' column. Aligning by nearest timestamp (hourly).")
    df_tab['time'] = pd.to_datetime(df_tab['time'])
    df_img['time'] = pd.to_datetime(df_img['time'])

    df_tab['time_h'] = df_tab['time'].dt.floor('H')
    df_img['time_h'] = df_img['time'].dt.floor('H')

    merged = pd.merge_asof(
        df_tab.sort_values('time_h'),
        df_img.sort_values('time_h'),
        on='time_h',
        direction='nearest',
        tolerance=pd.Timedelta('1H')
    )

    merged = merged.drop(columns=[c for c in ['time_h'] if c in merged.columns])
else:
    print("No 'time' column in both tables. Using simple repeat strategy.")
    n_tab = len(df_tab)
    n_img = len(df_img)
    if n_img == 0:
        raise SystemExit("No image features found.")

    repeats = (n_tab + n_img - 1) // n_img
    df_img_rep = (
        pd.concat([df_img] * repeats, ignore_index=True)
        .iloc[:n_tab]
        .reset_index(drop=True)
    )
    df_tab = df_tab.reset_index(drop=True)
    merged = pd.concat([df_tab, df_img_rep.add_prefix("img_")], axis=1)

print("Merged shape:", merged.shape)
print("Saving merged dataset to:", OUT_MERGED)
merged.to_csv(OUT_MERGED, index=False)
print("Done.")
