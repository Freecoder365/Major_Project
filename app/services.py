import joblib
import pandas as pd

from weather_summary import generate_weather_summary
from experiments.user_logic.agriculture_user import agriculture_user_output
from experiments.user_logic.travel_user import travel_user_output
from experiments.user_logic.event_user import event_user_output

RF_MODEL_PATH = "models/random_forest_multi.pkl"
XGB_MODEL_PATH = "models/xgb_multi.pkl"

rf = joblib.load(RF_MODEL_PATH)
xgb = joblib.load(XGB_MODEL_PATH)

def hybrid_prediction(input_dict):

    df = pd.DataFrame([input_dict])

    pred_rf = rf.predict(df)[0]
    pred_xgb = xgb.predict(df)[0]

    hybrid = {
        "temp": round((pred_rf[0]*0.4 + pred_xgb[0]*0.6), 2),
        "rhum": round((pred_rf[1]*0.4 + pred_xgb[1]*0.6), 2),
        "prcp": round((pred_rf[2]*0.5 + pred_xgb[2]*0.5), 2),
        "wspd": round((pred_rf[3]*0.5 + pred_xgb[3]*0.5), 2),
        "pres": round((pred_rf[4]*0.5 + pred_xgb[4]*0.5), 2),
    }

    return hybrid


def user_based_output(prediction, user_group):

    if user_group == "agriculture":
        return agriculture_user_output(prediction)

    elif user_group == "travel":
        return travel_user_output(prediction)

    elif user_group == "event":
        return event_user_output(prediction)

    else:
        return generate_weather_summary(prediction)
