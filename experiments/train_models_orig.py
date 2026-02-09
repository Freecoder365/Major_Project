# train_models.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
from config import PROCESSED_CSV
import os

# ------------------------------
# 1. Load & Clean Data
# ------------------------------
df = pd.read_csv(PROCESSED_CSV)
print(f"Data shape: {df.shape}")

# Drop duplicates
df = df.drop_duplicates()

# Drop non-numeric columns except lag/roll features
df = df.drop(columns=["time"])

# ------------------------------
# 2. Define features & targets
# ------------------------------
targets = ["temp", "rhum", "prcp", "wspd", "pres"]

features = [
    'dwpt', 'wdir', 'wspd', 'wpgt', 'hour', 'day_of_week', 'month',
    'temp_lag1', 'rhum_lag1', 'prcp_lag1', 'wspd_lag1', 'pres_lag1',
    'temp_roll3', 'rhum_roll3', 'prcp_roll3', 'wspd_roll3', 'pres_roll3'
]

X = df[features]
y = df[targets]

# ------------------------------
# 3. Train/Test Split
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training samples: {X_train.shape[0]}, Testing samples: {X_test.shape[0]}")

# ------------------------------
# 4. Evaluation Helper
# ------------------------------
def evaluate(model, name):
    preds = model.predict(X_test)
    results = {}
    for i, col in enumerate(y.columns):
        mae = mean_absolute_error(y_test.iloc[:, i], preds[:, i])
        rmse = mean_squared_error(y_test.iloc[:, i], preds[:, i]) ** 0.5
        results[col] = {"MAE": round(mae, 2), "RMSE": round(rmse, 2)}
    print(f"\n{name} Performance:")
    for col, vals in results.items():
        print(f"  {col:<10} -> MAE: {vals['MAE']}, RMSE: {vals['RMSE']}")
    return results

# ------------------------------
# 5. Train Models
# ------------------------------
rf = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42))
rf.fit(X_train, y_train)
evaluate(rf, "Random Forest")

xgb = MultiOutputRegressor(XGBRegressor(n_estimators=150, random_state=42, verbosity=0))
xgb.fit(X_train, y_train)
evaluate(xgb, "XGBoost")

# ------------------------------
# 6. Save Models
# ------------------------------
os.makedirs("models", exist_ok=True)
joblib.dump(rf, "models/random_forest_multi.pkl")
joblib.dump(xgb, "models/xgb_multi.pkl")
print("\n✅ Multi-parameter models saved successfully!")
