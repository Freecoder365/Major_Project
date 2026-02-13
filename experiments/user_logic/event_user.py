def event_user_output(prediction):
    rain = prediction["prcp"]
    wind = prediction["wspd"]
    temp = prediction["temp"]

    event_advisory = []
    event_risk = "Low"

    if rain > 5:
        event_advisory.append("High probability of rain. Outdoor events not advised.")
        event_risk = "High"
    elif rain > 0:
        event_advisory.append("Light rain possible. Keep backup arrangements.")
        event_risk = "Medium"
    else:
        event_advisory.append("No rainfall risk.")

    if wind > 20:
        event_advisory.append("Strong winds may disrupt stage setups.")
        event_risk = "High"

    if temp > 37:
        event_advisory.append("High temperature. Arrange cooling facilities.")

    return {
        "User Group": "Event Planning",
        "Risk Level": event_risk,
        "Event Advisory": event_advisory,
        "Recommendation": "Ensure backup indoor arrangements if required."
    }