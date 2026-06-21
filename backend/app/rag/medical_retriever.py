from app.rag.medical_documents import MEDICAL_DOCUMENTS


class MedicalRetriever:

    def retrieve(self, symptoms):
        retrieved_docs = []
        seen_ids = set()

        for symptom in symptoms:
            for document in MEDICAL_DOCUMENTS:
                if symptom.lower() in document["text"].lower():
                    if document["id"] not in seen_ids:
                        retrieved_docs.append(document)
                        seen_ids.add(document["id"])

        return retrieved_docs