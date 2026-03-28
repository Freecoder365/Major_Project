from agriculture_user import agriculture_user_output
from travel_user import travel_user_output
from event_user import event_user_output


def handle_query(user_group, prediction, query=None):
    """
    Routes the prediction to the correct user group
    and optionally answers a specific query.
    """

    if user_group.lower() == "agriculture":
        response = agriculture_user_output(prediction)

        if query:
            if "irrigation" in query.lower():
                if prediction["prcp"] > 1:
                    response += "\n🌾 Irrigation not required due to expected rainfall."
                else:
                    response += "\n🌾 Light irrigation recommended."

            elif "harvest" in query.lower():
                if prediction["prcp"] > 2:
                    response += "\n🌾 Not ideal for harvesting due to rainfall."
                else:
                    response += "\n🌾 Weather conditions suitable for harvesting."

    elif user_group.lower() == "travel":
        response = travel_user_output(prediction)

        if query:
            if "flight" in query.lower():
                if prediction["wspd"] > 20:
                    response += "\n✈️ High wind speed may cause flight delays."
                else:
                    response += "\n✈️ Weather conditions safe for flight operations."

            elif "road" in query.lower():
                if prediction["prcp"] > 2:
                    response += "\n🚗 Roads may be slippery due to rain."
                else:
                    response += "\n🚗 Road travel conditions are normal."

    elif user_group.lower() == "event":
        response = event_user_output(prediction)

        if query:
            if "outdoor" in query.lower():
                if prediction["prcp"] > 1:
                    response += "\n🎪 Outdoor event not recommended due to rain."
                else:
                    response += "\n🎪 Weather suitable for outdoor events."

    else:
        response = "❌ Invalid user group selected."

    return response


# -----------------------------------------------------
# RUN DEMO WHEN FILE EXECUTED DIRECTLY
# -----------------------------------------------------
if __name__ == "__main__":

    sample_prediction = {
        "temp": 28,
        "rhum": 60,
        "prcp": 1.5,
        "wspd": 15,
        "pres": 1008
    }

    print("\n--- AGRICULTURE QUERY ---")
    print(handle_query("agriculture", sample_prediction, "Is irrigation needed?"))

    print("\n--- TRAVEL QUERY ---")
    print(handle_query("travel", sample_prediction, "Is flight safe?"))

    print("\n--- EVENT QUERY ---")
    print(handle_query("event", sample_prediction, "Is outdoor event possible?"))
