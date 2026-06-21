class CaseSummaryBuilder:

    def should_generate_summary(self, asked_questions, symptoms, severity, duration):
        if len(asked_questions) >= 6:
            return True

        if symptoms and severity and duration and len(asked_questions) >= 4:
            return True

        return False

    def build_summary(self, symptoms, severity, duration, urgency, risk_factors, progression_factors):
        symptom_text = ", ".join(symptoms) if symptoms else "reported symptoms"
        risk_text = ", ".join(risk_factors) if risk_factors else "no major risk factors reported"
        progression_text = ", ".join(progression_factors) if progression_factors else "no clear progression details reported"

        return (
            f"Case summary:\n"
            f"- Symptoms: {symptom_text}\n"
            f"- Severity: {severity or 'not specified'}\n"
            f"- Duration: {duration or 'not specified'}\n"
            f"- Important details: {risk_text}\n"
            f"- Progression: {progression_text}\n\n"
            f"Urgency level:\n{urgency}\n\n"
            f"Recommendation:\n"
            f"{self._recommendation(urgency)}"
        )

    def _recommendation(self, urgency):
        if urgency == "EMERGENCY":
            return "Please seek emergency medical help immediately or contact local emergency services."

        if urgency == "HIGH":
            return "Please seek urgent medical evaluation as soon as possible."

        if urgency == "MODERATE":
            return "Consider contacting a healthcare professional, especially if symptoms continue, worsen, or affect daily activities."

        return "Monitor symptoms and seek medical advice if they continue, worsen, or new symptoms appear."