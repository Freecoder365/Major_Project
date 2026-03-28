from pydantic import BaseModel

class WeatherInput(BaseModel):
    dwpt: float
    wdir: float
    wspd: float
    hour: int
    day_of_week: int
    month: int
    temp_lag1: float
    rhum_lag1: float
    prcp_lag1: float
    wspd_lag1: float
    pres_lag1: float
    temp_roll3: float
    rhum_roll3: float
    prcp_roll3: float
    wspd_roll3: float
    pres_roll3: float
