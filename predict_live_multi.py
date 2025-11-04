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
