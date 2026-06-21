class ChatMemory:

    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id: str):

        if session_id not in self.sessions:

            self.sessions[session_id] = {
                "messages": [],
                "symptoms": [],
                "severity": None,
                "duration": None,
                "last_follow_up_question": None,
                "asked_questions": [],
                "risk_factors": [],
                "latest_risk_factors": [],
                "progression_factors": []
            }

    def get_session(self, session_id: str):

        self.create_session(session_id)

        return self.sessions[session_id]

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):

        session = self.get_session(session_id)

        session["messages"].append({
            "role": role,
            "content": content
        })

    def update_medical_context(
        self,
        session_id: str,
        symptoms=None,
        severity=None,
        duration=None
    ):

        session = self.get_session(session_id)

        if symptoms:

            for symptom in symptoms:

                if symptom not in session["symptoms"]:
                    session["symptoms"].append(symptom)

        if severity:
            session["severity"] = severity

        if duration:
            session["duration"] = duration

    def set_last_follow_up_question(
        self,
        session_id: str,
        question: str | None
    ):

        session = self.get_session(session_id)

        session["last_follow_up_question"] = question

    def add_asked_question(
        self,
        session_id: str,
        question: str | None
    ):

        if not question:
            return

        session = self.get_session(session_id)

        if question not in session["asked_questions"]:
            session["asked_questions"].append(question)

    def get_asked_questions(self, session_id: str):

        session = self.get_session(session_id)

        return session["asked_questions"]

    def add_risk_factors(
        self,
        session_id: str,
        risk_factors=None
    ):
        session = self.get_session(session_id)

        session["latest_risk_factors"] = []

        if not risk_factors:
            return

        for factor in risk_factors:

            if factor not in session["risk_factors"]:
                session["risk_factors"].append(factor)
                session["latest_risk_factors"].append(factor)


    def get_risk_factors(self, session_id: str):

        session = self.get_session(session_id)

        return session["risk_factors"]

    def get_latest_risk_factors(self, session_id: str):
        session = self.get_session(session_id)
        return session["latest_risk_factors"]

    def add_progression_factor(self, session_id: str, factor: str | None):
        if not factor:
            return

        session = self.get_session(session_id)

        if factor not in session["progression_factors"]:
            session["progression_factors"].append(factor)

    def get_progression_factors(self, session_id: str):
        session = self.get_session(session_id)
        return session["progression_factors"]

    def delete_session(self, session_id: str):

        if session_id in self.sessions:
            del self.sessions[session_id]

