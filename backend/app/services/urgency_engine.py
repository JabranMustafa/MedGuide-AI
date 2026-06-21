class UrgencyEngine:

    def calculate_urgency(self, symptoms, severity=None, risk_factors=None, progression_factors=None):
        risk_factors = risk_factors or []
        progression_factors = progression_factors or []

        if "difficulty breathing" in symptoms:
            if severity == "severe":
                return "EMERGENCY"
            return "HIGH"

        if "loss of consciousness" in symptoms:
            return "EMERGENCY"

        if "severe bleeding" in symptoms:
            return "EMERGENCY"

        if "confusion" in symptoms:
            return "EMERGENCY"

        if "stroke symptoms" in symptoms:
            return "EMERGENCY"

        if "chest pain" in symptoms and "dizziness" in symptoms:
            return "HIGH"

        if "chest pain" in symptoms:
            if severity == "severe":
                return "HIGH"
            return "MODERATE"

        if "back pain" in symptoms:
            if "numbness or weakness" in risk_factors:
                return "HIGH"

            if "pain radiating to leg" in risk_factors:
                return "MODERATE"

            if severity == "severe":
                return "MODERATE"

            return "LOW"

        if "eye pain" in symptoms:
            if severity == "severe":
                return "HIGH"
            return "MODERATE"

        if "abdominal pain" in symptoms:
            if severity == "severe":
                return "HIGH"
            return "MODERATE"

        if "headache" in symptoms and "stiff neck" in symptoms:
            return "HIGH"

        if "fever" in symptoms:
            return "MODERATE"

        if severity == "severe":
            return "MODERATE"

        if "symptoms getting worse" in progression_factors:
            return "MODERATE"

        return "LOW"