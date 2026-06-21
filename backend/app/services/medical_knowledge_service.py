import json
from pathlib import Path


class MedicalKnowledgeService:
    def __init__(self):
        base_dir = Path(__file__).resolve().parents[2]
        knowledge_path = base_dir / "data" / "medical_knowledge.json"

        with open(knowledge_path, "r", encoding="utf-8") as file:
            self.knowledge_base = json.load(file)

    def find_by_symptoms(self, symptoms):
        matched_items = []

        for symptom in symptoms:
            for item in self.knowledge_base:
                if symptom == item["symptom"]:
                    matched_items.append(item)

        return matched_items

    def build_explanation(self, symptoms):
        matched_items = self.find_by_symptoms(symptoms)

        if not matched_items:
            return (
                "These symptoms can have different possible causes. "
                "More details may help understand the situation better."
            )

        explanations = []

        for item in matched_items[:2]:
            causes = ", ".join(item["possible_causes"][:6])
            explanations.append(
                f"{item['symptom'].capitalize()} can be related to {causes}."
            )

        return " ".join(explanations)

    def get_follow_up_question(self, symptoms, asked_questions=None):
        asked_questions = asked_questions or []

        matched_items = self.find_by_symptoms(symptoms)

        if not matched_items:
            fallback_questions = [
                "Can you describe where the symptom is located?",
                "How long have you had this symptom?",
                "Would you describe it as mild, moderate, or severe?",
                "Is the symptom getting better, worse, or staying the same?"
            ]

            for question in fallback_questions:
                if question not in asked_questions:
                    return question

            return None

        all_questions = []

        for item in matched_items:
            all_questions.extend(item.get("follow_up_questions", []))

        generic_questions = [
            "How long have you had these symptoms?",
            "Would you describe the symptoms as mild, moderate, or severe?",
            "Are the symptoms getting better, worse, or staying the same?",
            "Did the symptoms start suddenly or gradually?",
            "Did anything trigger the symptoms?",
            "Do you have any other symptoms?",
            "Have you had this problem before?",
            "Does anything make it better or worse?",
            "Is the symptom affecting your daily activities?",
            "Have you recently had an injury, infection, or unusual physical activity?"
        ]

        all_questions.extend(generic_questions)

        for question in all_questions:
            if question not in asked_questions:
                return question

        return None
    def get_red_flags(self, symptoms):
        matched_items = self.find_by_symptoms(symptoms)

        red_flags = []

        for item in matched_items:
            red_flags.extend(item["red_flags"])

        return red_flags

    def get_sources(self, symptoms):
        matched_items = self.find_by_symptoms(symptoms)

        sources = []

        for item in matched_items:
            sources.append({
                "id": item["symptom"].replace(" ", "_") + "_001",
                "title": item["symptom"].capitalize() + " overview",
                "source": "Structured medical knowledge base"
            })

        return sources
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