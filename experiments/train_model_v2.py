# train_model_v2.py
"""
Hybrid training script: trains models on tabular + image features.
Saves models to experiments/models/
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

DATA_PATH = os.path.join("..", "data", "processed_with_images.csv")
OUT_DIR = "models"
os.makedirs(OUT_DIR, exist_ok=True)

print("Loading merged dataset:", DATA_PATH)
df = pd.read_csv(DATA_PATH)
print("Shape:", df.shape)

targets = ['temp', 'rhum', 'prcp', 'wspd', 'pres']
for t in targets:
    if t not in df.columns:
        raise SystemExit(f"Target {t} not found among columns.")

# drop non-numeric + time
drop_cols = targets + (['time'] if 'time' in df.columns else [])
X = df.drop(columns=drop_cols)
X = X.select_dtypes(include=['number'])
y = df[targets]

print("Feature columns:", X.columns.tolist())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Train / Test:", X_train.shape[0], X_test.shape[0])

print("Training RandomForest...")
rf = MultiOutputRegressor(
    RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
)
rf.fit(X_train, y_train)

print("Training XGBoost...")
xgb = MultiOutputRegressor(
    XGBRegressor(
        n_estimators=150,
        random_state=42,
        use_label_encoder=False,
        verbosity=0,
    )
)
xgb.fit(X_train, y_train)

def eval_model(m, name):
    preds = m.predict(X_test)
    print(f"\n{name} Performance:")
    for i, col in enumerate(y.columns):
        mae = mean_absolute_error(y_test.iloc[:, i], preds[:, i])
        rmse = mean_squared_error(y_test.iloc[:, i], preds[:, i]) ** 0.5
        print(f" {col:8s} -> MAE: {mae:.2f}, RMSE: {rmse:.2f}")

eval_model(rf, "RandomForest")
eval_model(xgb, "XGBoost")

joblib.dump(rf, os.path.join(OUT_DIR, "rf_hybrid.pkl"))
joblib.dump(xgb, os.path.join(OUT_DIR, "xgb_hybrid.pkl"))
print("Saved models to", OUT_DIR)
