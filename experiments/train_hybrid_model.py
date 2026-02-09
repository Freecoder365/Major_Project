# experiments/train_hybrid_model.py
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import StackingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

TRAIN_CSV = os.path.join("..","data","processed.csv")   # existing processed file
IMAGE_CSV = os.path.join("..","data","image_features.csv")  # optional
OUT_DIR = "models"
OUT_MODEL = os.path.join(OUT_DIR, "hybrid_weather_model.pkl")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs("experiments/models", exist_ok=True)

print("🔹 Loading training data:", TRAIN_CSV)
df = pd.read_csv(TRAIN_CSV)

# Ensure target columns exist
targets = ['temp','rhum','prcp','wspd','pres']
for t in targets:
    if t not in df.columns:
        raise SystemExit(f"Target '{t}' not found in {TRAIN_CSV}")

# Merge image features if available (simple alignment)
if os.path.exists(IMAGE_CSV):
    print("🔹 Found image features:", IMAGE_CSV, "— merging by repeating/trimming to match length.")
    img = pd.read_csv(IMAGE_CSV).reset_index(drop=True)
    # repeat images to match length if needed (simple strategy)
    rep = pd.concat([img]*((len(df)//len(img))+1), ignore_index=True).iloc[:len(df)].reset_index(drop=True)
    rep = rep.drop(columns=['image'], errors='ignore')
    df = pd.concat([df.reset_index(drop=True), rep.reset_index(drop=True)], axis=1)
else:
    print("🔹 No image features found — training with numeric features only.")

# Prepare X, y
X = df.drop(columns=targets + ['time'], errors='ignore')
y = df[targets]
X = X.fillna(0)
y = y.fillna(0)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Training samples:", X_train.shape, "Testing:", X_test.shape)

# Base learners
rf = RandomForestRegressor(n_estimators=150, random_state=42)
xgb = XGBRegressor(n_estimators=200, learning_rate=0.05, random_state=42)

# Stacking regressor as final estimator wrapped for multioutput
stack = MultiOutputRegressor(StackingRegressor(
    estimators=[('rf', rf), ('xgb', xgb)],
    final_estimator=RidgeCV()
))

print("🔹 Training stacking hybrid model ... (this may take a little)")
stack.fit(X_train, y_train)

# Evaluate per-target
preds = stack.predict(X_test)
print("\nEvaluation:")
for i, col in enumerate(y.columns):
    mae = mean_absolute_error(y_test.iloc[:, i], preds[:, i])
    r2 = r2_score(y_test.iloc[:, i], preds[:, i])
    print(f" {col:<6} -> MAE: {mae:.3f}, R2: {r2:.3f}")

# Save
joblib.dump(stack, os.path.join("experiments","models","hybrid_weather_model.pkl"))
print(f"\n💾 Saved hybrid model to experiments/models/hybrid_weather_model.pkl")
