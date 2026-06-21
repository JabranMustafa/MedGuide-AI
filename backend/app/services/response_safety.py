class ResponseSafety:

    def clean_response(self, response: str, symptoms=None, retrieved_docs=None) -> str:
        symptoms = symptoms or []
        retrieved_docs = retrieved_docs or []

        if not response:
            return self.fallback_response(symptoms, retrieved_docs)

        bad_patterns = [
            "[Patient]",
            "[MedGuide]",
            "Jane Doe",
            "TASK:",
            "DO NOT:",
            "OUTPUT FORMAT",
            "You are MedGuide AI",
            "Rules:",
            "Rule(s):",
            "PATIENT DATA",
            "USER MESSAGE",
            "Question:",
            "Suggested short answer",
            "Trusted Context:",
            "Symptoms:",
            "Duration:",
            "diagnosis",
            "prescribe medication"
            "According to the given text",
            "short possible explanation",
            "Severe fever",
            "over 39",
            "over 41",
            "treatment options",
            "plan for treatment"
        ]

        for pattern in bad_patterns:
            if pattern.lower() in response.lower():
                return self.fallback_response(symptoms, retrieved_docs)

        if len(response) > 600:
            return self.fallback_response(symptoms, retrieved_docs)

        return response.strip()

    def fallback_response(self, symptoms, retrieved_docs):
        if retrieved_docs:
            context_sentences = []

            for doc in retrieved_docs:
                text = doc.get("text", "")
                first_sentence = text.split(".")[0].strip()

                if first_sentence:
                    context_sentences.append(first_sentence + ".")

            if context_sentences:
                return " ".join(context_sentences[:2])

        if symptoms:
            symptom_text = ", ".join(symptoms)
            return (
                f"{symptom_text.capitalize()} can have different possible causes. "
                "More details such as duration, severity, and additional symptoms can help guide urgency."
            )

        return (
            "These symptoms can have different possible causes. "
            "More details such as duration, severity, and additional symptoms can help guide urgency."
        )