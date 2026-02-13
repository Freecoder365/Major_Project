import pandas as pd
import joblib
from config import PROCESSED_CSV
import warnings

warnings.filterwarnings("ignore")

# Paths
RF_MODEL_PATH = "models/random_forest_multi.pkl"
XGB_MODEL_PATH = "models/xgb_multi.pkl"
LIVE_PROCESSED_PATH = "data/live_data_processed.csv"

print("🔹 Loading trained models...")
rf = joblib.load(RF_MODEL_PATH)
xgb = joblib.load(XGB_MODEL_PATH)

# Load training and live data
train_df = pd.read_csv(PROCESSED_CSV)
live_df = pd.read_csv(LIVE_PROCESSED_PATH)

print("\nUsing latest live data for prediction:")
print(live_df.head(), "\n")

# Align columns to match model training features (include wspd!)
X_cols = [c for c in train_df.columns if c not in ['temp', 'rhum', 'prcp', 'pres', 'time']]
X_live = live_df[X_cols]

print("🔹 Making predictions...")
print("Columns used for prediction:", X_live.columns.tolist())

# Predict
pred_rf = rf.predict(X_live)[0]
pred_xgb = xgb.predict(X_live)[0]

targets = ['temp', 'rhum', 'prcp', 'wspd', 'pres']

print("\n✅ Predictions:")
print("Random Forest →", {t: round(p, 2) for t, p in zip(targets, pred_rf)})
print("XGBoost       →", {t: round(p, 2) for t, p in zip(targets, pred_xgb)})

from weather_summary import generate_weather_summary

rf_summary = generate_weather_summary(
    dict(zip(targets, pred_rf))
)

xgb_summary = generate_weather_summary(
    dict(zip(targets, pred_xgb))
)

print("\n🗣️ User-Friendly Weather Summary:")
print("Random Forest:", rf_summary)
print("XGBoost:", xgb_summary)

# ---- Hybrid Ensemble (Weighted Average) ----
hybrid_pred = {
    "temp": round((pred_rf[0] * 0.4 + pred_xgb[0] * 0.6), 2),
    "rhum": round((pred_rf[1] * 0.4 + pred_xgb[1] * 0.6), 2),
    "prcp": round((pred_rf[2] * 0.5 + pred_xgb[2] * 0.5), 2),
    "wspd": round((pred_rf[3] * 0.5 + pred_xgb[3] * 0.5), 2),
    "pres": round((pred_rf[4] * 0.5 + pred_xgb[4] * 0.5), 2),
}

print("\n🔶 Final Hybrid Prediction (Best Estimate):")
print(hybrid_pred)

from weather_summary import generate_weather_summary

print("\n🧠 Final User-Friendly Forecast (Hybrid Model):")
print(generate_weather_summary(hybrid_pred, "Hybrid Model"))



import pandas as pd
import joblib
from config import PROCESSED_CSV
import warnings

warnings.filterwarnings("ignore")

# ----------------------------
# Paths
# ----------------------------
RF_MODEL_PATH = "models/random_forest_multi.pkl"
XGB_MODEL_PATH = "models/xgb_multi.pkl"
LIVE_PROCESSED_PATH = "data/live_data_processed.csv"
LIVE_IMAGE_FEATURES_PATH = "data/live_image_features.csv"

print("🔹 Loading trained models...")
rf = joblib.load(RF_MODEL_PATH)
xgb = joblib.load(XGB_MODEL_PATH)

# ----------------------------
# Load training & live data
# ----------------------------
train_df = pd.read_csv(PROCESSED_CSV)
live_df = pd.read_csv(LIVE_PROCESSED_PATH)

print("\nUsing latest live weather data:")
print(live_df.head(), "\n")

# ----------------------------
# 🔹 NEW: Load live image features
# ----------------------------
try:
    img_df = pd.read_csv(LIVE_IMAGE_FEATURES_PATH)
    print("🖼️ Live image features loaded:")
    print(img_df.head(), "\n")

    # Take latest image features
    img_features = img_df.iloc[-1][["img_brightness", "img_cloud_density"]]

    # Add image features to live data
    live_df["img_brightness"] = img_features["img_brightness"]
    live_df["img_cloud_density"] = img_features["img_cloud_density"]

except Exception as e:
    print("⚠️ Live image features not found. Using defaults.")
    live_df["img_brightness"] = 0
    live_df["img_cloud_density"] = 0

# ----------------------------
# Align columns with training
# ----------------------------
X_cols = [
    c for c in train_df.columns
    if c not in ['temp', 'rhum', 'prcp', 'pres', 'time']
]

# Ensure all required columns exist
for col in X_cols:
    if col not in live_df.columns:
        live_df[col] = 0

X_live = live_df[X_cols]

print("🔹 Making predictions...")
print("Columns used for prediction:", X_live.columns.tolist())

# ----------------------------
# Predict
# ----------------------------
pred_rf = rf.predict(X_live)[0]
pred_xgb = xgb.predict(X_live)[0]

targets = ['temp', 'rhum', 'prcp', 'wspd', 'pres']

print("\n✅ Predictions:")
print("Random Forest →", {t: round(p, 2) for t, p in zip(targets, pred_rf)})
print("XGBoost       →", {t: round(p, 2) for t, p in zip(targets, pred_xgb)})

# ----------------------------
# User-friendly summaries
# ----------------------------
from weather_summary import generate_weather_summary

rf_summary = generate_weather_summary(dict(zip(targets, pred_rf)))
xgb_summary = generate_weather_summary(dict(zip(targets, pred_xgb)))

print("\n🗣️ User-Friendly Weather Summary:")
print("Random Forest:", rf_summary)
print("XGBoost:", xgb_summary)

# ----------------------------
# 🔶 Hybrid Ensemble
# ----------------------------
hybrid_pred = {
    "temp": round((pred_rf[0] * 0.4 + pred_xgb[0] * 0.6), 2),
    "rhum": round((pred_rf[1] * 0.4 + pred_xgb[1] * 0.6), 2),
    "prcp": round((pred_rf[2] * 0.5 + pred_xgb[2] * 0.5), 2),
    "wspd": round((pred_rf[3] * 0.5 + pred_xgb[3] * 0.5), 2),
    "pres": round((pred_rf[4] * 0.5 + pred_xgb[4] * 0.5), 2),
}

print("\n🔶 Final Hybrid Prediction (Best Estimate):")
print(hybrid_pred)

print("\n🧠 Final User-Friendly Forecast (Hybrid Model):")
print(generate_weather_summary(hybrid_pred, "Hybrid Model"))

# ================= USER GROUP LOGIC =================
from experiments.user_logic.travel_user import travel_user_output
from experiments.user_logic.agriculture_user import agriculture_user_output
from experiments.user_logic.event_user import event_user_output

print("\n================ USER GROUP SPECIFIC OUTPUTS ================\n")

print("✈️ Travel / Flight User:")
print(travel_user_output(hybrid_pred))

print("\n🌾 Agriculture User:")
print(agriculture_user_output(hybrid_pred))

print("\n🎉 Event Planning User:")
print(event_user_output(hybrid_pred))

