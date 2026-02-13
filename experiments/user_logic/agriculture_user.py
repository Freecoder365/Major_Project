def agriculture_user_output(prediction):
    humidity = prediction["rhum"]
    rain = prediction["prcp"]
    temp = prediction["temp"]

    farming_advice = []
    risk = "Low"

    if rain > 10:
        farming_advice.append("Heavy rainfall expected. Risk of waterlogging.")
        risk = "High"
    elif rain > 3:
        farming_advice.append("Moderate rainfall beneficial for crops.")
    else:
        farming_advice.append("No rainfall expected. Plan irrigation.")

    if humidity > 80:
        farming_advice.append("High humidity increases fungal infection risk.")
        risk = "Medium"

    if temp > 35:
        farming_advice.append("Heat stress possible for crops.")
        risk = "Medium"

    return {
        "User Group": "Agriculture",
        "Risk Level": risk,
        "Crop Advisory": farming_advice,
        "Recommendation": "Adjust irrigation and pesticide schedule accordingly."
    }