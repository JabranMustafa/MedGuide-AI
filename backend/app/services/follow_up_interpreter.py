class FollowUpInterpreter:

    def interpret(self, user_message: str, last_question: str | None):
        result = {
            "extra_symptoms": [],
            "risk_factors": []
        }

        if not last_question:
            return result

        text = user_message.lower().strip()

        yes_words = ["yes", "yeah", "yep", "i have", "also", "sometimes"]
        no_words = ["no", "not", "nope", "dont", "don't"]

        is_yes = any(word in text for word in yes_words)
        is_no = any(word in text for word in no_words)

        if is_no or not is_yes:
            return result

        question = last_question.lower()

        if "pain go down your leg" in question:
            result["extra_symptoms"].extend(["leg pain", "nerve irritation concern"])
            result["risk_factors"].append("pain radiating to leg")

        elif "numbness or weakness" in question:
            result["extra_symptoms"].extend(["numbness", "weakness"])
            result["risk_factors"].append("numbness or weakness")

        elif "injury or heavy lifting" in question:
            result["risk_factors"].append("started after injury or heavy lifting")

        elif "blurred vision" in question:
            result["extra_symptoms"].append("blurred vision")
            result["risk_factors"].append("blurred vision")

        elif "breathing difficulty" in question:
            result["extra_symptoms"].append("difficulty breathing")
            result["risk_factors"].append("breathing difficulty")

        elif "dizziness" in question:
            result["extra_symptoms"].append("dizziness")
            result["risk_factors"].append("dizziness")

        elif "neck stiffness" in question:
            result["extra_symptoms"].append("stiff neck")
            result["risk_factors"].append("neck stiffness")

        return result