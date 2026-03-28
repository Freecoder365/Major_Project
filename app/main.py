from fastapi import FastAPI
from app.schemas import WeatherInput
from app.services import hybrid_prediction, user_based_output

app = FastAPI(title="Hyperlocal Weather API")

@app.get("/")
def root():
    return {"status": "API running successfully"}

@app.post("/predict")
def predict_weather(data: WeatherInput, user_group: str = "general"):

    prediction = hybrid_prediction(data.dict())
    advisory = user_based_output(prediction, user_group)

    return {
        "prediction": prediction,
        "advisory": advisory
    }
