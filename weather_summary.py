def generate_weather_summary(pred, model_name="Model"):
    """
    Converts numerical weather predictions into
    easy-to-understand English descriptions with practical suggestions.
    """

    temp = float(pred["temp"])
    rhum = float(pred["rhum"])
    prcp = float(pred["prcp"])
    wspd = float(pred["wspd"])

    summary = []
    tags = []

    # 🌡️ TEMPERATURE TYPES
    if temp < 15:
        tags.append("Cold")
        summary.append("It will be quite cold today.")
        summary.append("Wear a warm jacket, sweater, or full winter clothing.")
    elif 15 <= temp < 22:
        tags.append("Cool")
        summary.append("The weather will be cool and comfortable.")
        summary.append("Light winter wear or full sleeves should be sufficient.")
    elif 22 <= temp < 28:
        tags.append("Pleasant")
        summary.append("The day will be pleasant and comfortable.")
        summary.append("Ideal weather for outdoor activities and travel.")
    elif 28 <= temp < 33:
        tags.append("Warm")
        summary.append("It will feel warm during the day.")
        summary.append("Wear light cotton clothes and drink enough water.")
    else:
        tags.append("Hot")
        summary.append("It will be very hot today.")
        summary.append("Avoid outdoor activities during noon and stay hydrated.")

    # 💧 HUMIDITY TYPES
    if rhum >= 75:
        tags.append("Humid")
        summary.append("The air will feel humid and slightly uncomfortable.")
        summary.append("Sweating may increase, so stay hydrated.")
    elif rhum <= 30:
        tags.append("Dry")
        summary.append("The air will feel dry.")
        summary.append("Drink water regularly and use moisturizers if needed.")
    else:
        tags.append("Comfortable Humidity")
        summary.append("Humidity levels will be comfortable.")

    # 🌧️ RAIN TYPES
    if prcp >= 5:
        tags.append("Heavy Rain")
        summary.append("Heavy rainfall is expected.")
        summary.append("Avoid unnecessary travel and carry proper rain protection.")
    elif 1 <= prcp < 5:
        tags.append("Rainy")
        summary.append("Moderate rainfall is expected.")
        summary.append("Carry an umbrella or raincoat when going out.")
    elif 0.1 <= prcp < 1:
        tags.append("Light Rain")
        summary.append("There may be light rainfall.")
        summary.append("An umbrella may be useful just in case.")
    else:
        tags.append("Dry")
        summary.append("No rainfall is expected today.")

    # 🌬️ WIND TYPES
    if wspd >= 10:
        tags.append("Windy")
        summary.append("Strong winds are expected.")
        summary.append("Be cautious while riding two-wheelers or driving.")
    elif 4 <= wspd < 10:
        tags.append("Breezy")
        summary.append("A pleasant breeze can be expected.")
    else:
        tags.append("Calm")
        summary.append("Winds will be light and calm.")

    # ☀️ SUNNY / IDEAL DAY IDENTIFICATION
    if (
        prcp == 0
        and 22 <= temp <= 28
        and rhum < 70
        and wspd < 8
    ):
        tags.append("Ideal Day")
        summary.append(
            "Overall, the weather is ideal for stepping out, traveling, or enjoying outdoor activities."
        )

    # 🏷️ Final formatted output
    weather_type = ", ".join(sorted(set(tags)))
    final_text = (
        f"{model_name} Prediction Summary:\n"
        f"Expected Weather Types: {weather_type}\n"
        + " ".join(summary)
    )

    return final_text
