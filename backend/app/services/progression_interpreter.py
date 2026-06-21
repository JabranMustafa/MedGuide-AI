class ProgressionInterpreter:

    def interpret(self, user_message: str, severity=None, duration=None):
        text = user_message.lower()

        factors = []

        if duration:
            factors.append(f"symptoms lasting {duration}")

        if severity == "severe":
            factors.append("severe symptom intensity")

        if "worse" in text or "worsening" in text or "getting worse" in text:
            factors.append("symptoms getting worse")

        if "better" in text or "improving" in text:
            factors.append("symptoms improving")

        if "same" in text or "not changing" in text:
            factors.append("symptoms staying the same")

        if "suddenly" in text or "sudden" in text:
            factors.append("sudden onset")

        if "gradually" in text or "slowly" in text:
            factors.append("gradual onset")

        return factors