# ================================
# Project Configuration File
# Hyperlocal Weather Forecasting
# Location: Lohegaon, Pune
# ================================

# ---- Location Coordinates ----
LAT = 18.5793
LON = 73.9089

# ---- Data File Paths ----
HISTORICAL_CSV = "data/historical.csv"
RAW_CSV = "data/raw_weather_data.csv"
PROCESSED_CSV = "data/processed.csv"

# ---- Live Data Files (API) ----
LIVE_DATA_CSV = "data/live_data.csv"
LIVE_DATA_JSON = "data/live_data.json"
LIVE_DATA_PROCESSED = "data/live_data_processed.csv"

# ---- Image Feature Data ----
IMAGE_FEATURES_CSV = "data/image_features.csv"
PROCESSED_WITH_IMAGES = "data/processed_with_images.csv"

# ---- Model Paths ----
MODEL_DIR = "models/"

RF_MODEL_PATH = MODEL_DIR + "random_forest_multi.pkl"
XGB_MODEL_PATH = MODEL_DIR + "xgb_multi.pkl"

RF_HYBRID_MODEL_PATH = MODEL_DIR + "rf_hybrid.pkl"
XGB_HYBRID_MODEL_PATH = MODEL_DIR + "xgb_hybrid.pkl"

