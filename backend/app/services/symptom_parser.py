import re
from app.services.symptom_vocabulary import SYMPTOM_SYNONYMS


class SymptomParser:
    def __init__(self):
        self.symptom_synonyms = SYMPTOM_SYNONYMS

        self.body_parts = {
            "heart": "chest pain",
            "chest": "chest pain",
            "back": "back pain",
            "eye": "eye pain",
            "eyes": "eye pain",
            "head": "headache",
            "throat": "sore throat",
            "stomach": "abdominal pain",
            "belly": "abdominal pain",
            "tummy": "abdominal pain",
            "abdomen": "abdominal pain",
            "butt": "buttock pain",
            "butts": "buttock pain",
            "buttock": "buttock pain",
            "leg": "leg pain",
            "legs": "leg pain",
            "arm": "arm pain",
            "arms": "arm pain",
            "neck": "neck pain",
            "shoulder": "shoulder pain",
            "shoulders": "shoulder pain",
            "ear": "ear pain",
            "ears": "ear pain",
            "tooth": "tooth pain",
            "teeth": "tooth pain",
            "knee": "knee pain",
            "knees": "knee pain",
            "foot": "foot pain",
            "feet": "foot pain",
            "hand": "hand pain",
            "hands": "hand pain",
            "liver": "liver area pain",
            "right abdomen": "liver area pain",
            "right side": "liver area pain",
                          "backbone": "back pain",
        "spine": "back pain"
        }

        self.disease_concerns = {
            "corona": "respiratory infection concern",
            "covid": "respiratory infection concern",
            "covid-19": "respiratory infection concern",
            "flu": "flu-like symptoms",
            "infection": "infection concern",
            "allergy": "allergy concern",
            "asthma": "breathing concern",
            "heart attack": "chest pain",
            "stroke": "stroke symptoms",
            "liver problem": "liver area pain",
            "liver disease": "liver area pain",
            "hepatitis": "liver area pain",
            "jaundice": "liver area pain"
        }

        self.severity_words = {
            "mild": [
                "mild", "little", "slight", "small pain",
                "not much", "light pain"
            ],
            "moderate": [
                "moderate", "medium", "normal pain",
                "not too much"
            ],
            "severe": [
                "severe", "very bad", "too much",
                "strong pain", "unbearable", "worst",
                "extreme", "intense"
            ]
        }

    def extract_symptoms(self, text: str) -> dict:
        normalized_text = self._normalize_text(text)

        symptoms = []

        symptoms.extend(self._extract_from_synonyms(normalized_text))
        symptoms.extend(self._extract_body_part_pain(normalized_text))
        symptoms.extend(self._extract_disease_concerns(normalized_text))

        symptoms = self._remove_duplicates(symptoms)

        severity = self._extract_severity(normalized_text)
        duration = self._extract_duration(normalized_text)

        return {
            "symptoms": symptoms,
            "severity": severity,
            "duration": duration
        }

    def _normalize_text(self, text: str) -> str:
        text = text.lower()
        text = text.replace("can't", "cant")
        text = text.replace("cannot", "cant")
        text = re.sub(r"[^a-z0-9\s\-]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _extract_from_synonyms(self, text: str) -> list:
        detected = []

        for symptom, synonyms in self.symptom_synonyms.items():
            for synonym in synonyms:
                if synonym in text:
                    detected.append(symptom)
                    break

        return detected

    def _extract_body_part_pain(self, text: str) -> list:
        detected = []

        for body_word, mapped_symptom in self.body_parts.items():
            patterns = [
                f"pain in my {body_word}",
                f"pain in the {body_word}",
                f"pain in {body_word}",
                f"my {body_word} hurts",
                f"{body_word} hurts",
                f"{body_word} pain",
                f"sore {body_word}"
            ]

            for pattern in patterns:
                if pattern in text:
                    detected.append(mapped_symptom)
                    break

        return detected

    def _extract_disease_concerns(self, text: str) -> list:
        detected = []

        for disease_word, mapped_symptom in self.disease_concerns.items():
            if disease_word in text:
                detected.append(mapped_symptom)

        return detected

    def _extract_severity(self, text: str):
        for severity, words in self.severity_words.items():
            for word in words:
                if word in text:
                    return severity

        return None

    def _extract_duration(self, text: str):
        pattern = r"\b(\d+)\s*(hour|hours|day|days|week|weeks|month|months)\b"
        match = re.search(pattern, text)

        if match:
            return f"{match.group(1)} {match.group(2)}"

        return None

    def _remove_duplicates(self, items: list) -> list:
        unique_items = []

        for item in items:
            if item not in unique_items:
                unique_items.append(item)

        return unique_items
