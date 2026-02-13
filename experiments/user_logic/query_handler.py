def handle_user_query(user_type, query, prediction):
    query = query.lower()

    if user_type == "agriculture":
        if "irrigate" in query:
            if prediction["prcp"] > 3:
                return "Rain expected. Irrigation may not be required."
            else:
                return "No rainfall expected. Irrigation recommended."

    if user_type == "travel":
        if "flight" in query or "safe" in query:
            if prediction["wspd"] > 20 or prediction["prcp"] > 5:
                return "Weather conditions may cause delays. Monitor updates."
            else:
                return "Weather conditions are suitable for travel."

    if user_type == "event":
        if "outdoor" in query:
            if prediction["prcp"] > 2:
                return "Outdoor event not recommended due to rain risk."
            else:
                return "Weather conditions suitable for outdoor event."

    return "Query not recognized for selected user group."