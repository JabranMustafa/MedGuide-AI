class ChatResponseBuilder:

    def build_reply(
        self,
        explanation: str,
        urgency: str,
        follow_up_question: str | None,
        risk_factors=None,
        progression_factors=None
    ) -> str:

        risk_factors = risk_factors or []
        progression_factors = progression_factors or []

        recommendation = self.get_recommendation(
            urgency=urgency,
            risk_factors=risk_factors,
            progression_factors=progression_factors
        )

        reply = (
            f"Possible explanation:\n{explanation}\n\n"
            f"Urgency level:\n{urgency}\n\n"
            f"Recommendation:\n{recommendation}"
        )

        if follow_up_question:
            reply += f"\n\nFollow-up question:\n{follow_up_question}"

        return reply

    def get_recommendation(
        self,
        urgency: str,
        risk_factors=None,
        progression_factors=None
    ) -> str:

        risk_factors = risk_factors or []
        progression_factors = progression_factors or []

        if urgency == "EMERGENCY":
            return (
                "Please seek emergency medical help immediately or contact local emergency services."
            )

        if urgency == "HIGH":
            return (
                "Please seek urgent medical evaluation as soon as possible, especially because your answers include higher-risk features."
            )

        if "numbness or weakness" in risk_factors:
            return (
                "Consider contacting a healthcare professional soon, especially because numbness or weakness can suggest nerve involvement."
            )

        if "pain radiating to leg" in risk_factors:
            return (
                "Consider medical advice if the pain continues, worsens, or affects walking, because pain spreading to the leg can sometimes involve nerve irritation."
            )

        if "symptoms getting worse" in progression_factors:
            return (
                "Because symptoms are getting worse, consider contacting a healthcare professional for further guidance."
            )

        if urgency == "MODERATE":
            return (
                "Consider contacting a healthcare professional, especially if symptoms continue, worsen, or new symptoms appear."
            )

        return (
            "Monitor your symptoms. If they worsen or continue, consider contacting a healthcare professional."
        )