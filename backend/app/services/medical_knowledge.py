MEDICAL_KNOWLEDGE = {

    "fever": {
        "description": (
            "Fever can occur due to infections, inflammation, "
            "or immune system responses."
        )
    },

    "headache": {
        "description": (
            "Headaches can have many causes including stress, "
            "dehydration, migraines, or infections."
        )
    },

    "chest pain": {
        "description": (
            "Chest pain can sometimes be associated with serious "
            "medical conditions and should not be ignored."
        )
    },

    "dizziness": {
        "description": (
            "Dizziness may occur due to dehydration, low blood pressure, "
            "inner ear issues, or other medical conditions."
        )
    },

    "difficulty breathing": {
        "description": (
            "Difficulty breathing may indicate a serious condition "
            "requiring urgent medical evaluation."
        )
    }
}
def build_explanation_with_context(self, symptoms, risk_factors=None):
    risk_factors = risk_factors or []

    base_explanation = self.build_explanation(symptoms)

    if not risk_factors:
        return base_explanation

    risk_text = ", ".join(risk_factors)

    return (
        f"{base_explanation} "
        f"Your follow-up answers mention {risk_text}, which may suggest that the symptoms need closer attention."
    )