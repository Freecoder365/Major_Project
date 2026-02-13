def travel_user_output(prediction):
    wind = prediction["wspd"]
    rain = prediction["prcp"]
    temp = prediction["temp"]
    humidity = prediction["rhum"]

    advisory = []
    risk_level = "Low"

    # Wind Analysis
    if wind > 25:
        advisory.append("High wind speeds detected. Strong turbulence possible.")
        risk_level = "High"
    elif wind > 15:
        advisory.append("Moderate winds expected. Minor turbulence possible.")
        risk_level = "Medium"
    else:
        advisory.append("Wind conditions are stable for flight operations.")

    # Rain Analysis
    if rain > 5:
        advisory.append("Heavy rainfall expected. Runway delays likely.")
        risk_level = "High"
    elif rain > 0:
        advisory.append("Light rainfall expected. Slight visibility reduction.")
        if risk_level != "High":
            risk_level = "Medium"
    else:
        advisory.append("No rainfall expected.")

    # Temperature impact
    if temp > 38:
        advisory.append("High ground temperature may affect aircraft performance.")

    return {
        "User Group": "Travel / Flight",
        "Risk Level": risk_level,
        "Detailed Advisory": advisory,
        "Recommendation": "Check flight status 2 hours before departure and monitor updates."
    }