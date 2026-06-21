class ConversationReasoner:

    def generate_turn_insight(self, symptoms, risk_factors, latest_risk_factors):
        if not latest_risk_factors:
            return None

        insights = []

        for factor in latest_risk_factors:

            if factor == "pain radiating to leg":
                insights.append(
                    "Pain going down the leg can sometimes happen when a nerve in the lower back is irritated or compressed."
                )

            elif factor == "numbness or weakness":
                insights.append(
                    "Back pain together with numbness or weakness can suggest stronger nerve involvement and may need closer medical evaluation."
                )

            elif factor == "started after injury or heavy lifting":
                insights.append(
                    "Symptoms that start after injury or heavy lifting can be related to muscle strain, disc irritation, or other mechanical back problems."
                )

            elif factor == "breathing difficulty":
                insights.append(
                    "Breathing difficulty together with other symptoms can increase urgency and should be taken seriously."
                )

            elif factor == "blurred vision":
                insights.append(
                    "Eye pain with blurred vision can be more concerning than eye pain alone and may need prompt medical evaluation."
                )

            elif factor == "dizziness":
                insights.append(
                    "Dizziness together with other symptoms can increase concern, especially if it occurs with chest pain, weakness, or fainting."
                )

        if insights:
            return " ".join(insights)

        return None

    def generate_progression_insight(self, progression_factors):
        if not progression_factors:
            return None

        latest_factor = progression_factors[-1]

        if "symptoms lasting" in latest_factor:
            return (
                f"Because the symptoms have lasted {latest_factor.replace('symptoms lasting ', '')}, "
                "it may be useful to monitor whether they are improving, worsening, or affecting daily activity."
            )

        if latest_factor == "severe symptom intensity":
            return (
                "Severe symptom intensity can make the situation more concerning, especially when combined with radiating pain, numbness, or weakness."
            )

        if latest_factor == "symptoms getting worse":
            return (
                "Symptoms that are getting worse over time may need closer medical attention, especially when combined with pain spreading to the leg or numbness."
            )

        if latest_factor == "symptoms improving":
            return (
                "Improving symptoms can be a reassuring sign, but they should still be monitored if they return or interfere with daily activities."
            )

        if latest_factor == "symptoms staying the same":
            return (
                "Symptoms that are not improving may still need attention if they continue or affect movement, sleep, or daily activities."
            )

        if latest_factor == "sudden onset":
            return (
                "Symptoms that start suddenly can sometimes suggest injury, strain, or nerve irritation, depending on what happened before the pain began."
            )

        if latest_factor == "gradual onset":
            return (
                "Symptoms that develop gradually can sometimes be related to posture, repeated strain, or ongoing irritation."
            )

        return None