from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    SymptomRequest,
    SymptomResponse,
    ChatRequest,
    ChatResponse
)

from app.services.symptom_parser import SymptomParser
from app.services.urgency_engine import UrgencyEngine
from app.services.response_safety import ResponseSafety
from app.services.chat_memory import ChatMemory
from app.services.chat_response_builder import ChatResponseBuilder
from app.services.medical_knowledge_service import MedicalKnowledgeService
from app.services.follow_up_interpreter import FollowUpInterpreter
from app.services.conversation_reasoner import ConversationReasoner
from app.services.progression_interpreter import ProgressionInterpreter
from app.services.case_summary_builder import CaseSummaryBuilder
app = FastAPI(title="MedGuide AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


symptom_parser = SymptomParser()
urgency_engine = UrgencyEngine()
response_safety = ResponseSafety()
chat_memory = ChatMemory()
chat_response_builder = ChatResponseBuilder()
medical_knowledge_service = MedicalKnowledgeService()
follow_up_interpreter = FollowUpInterpreter()
conversation_reasoner = ConversationReasoner()
progression_interpreter = ProgressionInterpreter()
case_summary_builder = CaseSummaryBuilder()
DISCLAIMER = (
    "This tool is for educational purposes only and "
    "is not a substitute for professional medical advice."
)


@app.post("/analyze-symptoms", response_model=SymptomResponse)
def analyze_symptoms(request: SymptomRequest):

    parsed_data = symptom_parser.extract_symptoms(request.message)

    symptoms = parsed_data["symptoms"]
    severity = parsed_data["severity"]
    duration = parsed_data["duration"]

    urgency = urgency_engine.calculate_urgency(
        symptoms=symptoms,
        severity=severity
    )

    retrieved_docs = medical_knowledge_service.get_sources(symptoms)
    explanation = medical_knowledge_service.build_explanation(symptoms)

    explanation = response_safety.clean_response(
        response=explanation,
        symptoms=symptoms,
        retrieved_docs=retrieved_docs
    )

    return SymptomResponse(
        symptoms=symptoms,
        severity=severity,
        duration=duration,
        urgency=urgency,
        explanation=explanation,
        disclaimer=DISCLAIMER,
        sources=[
            {
                "id": doc["id"],
                "title": doc["title"],
                "source": doc["source"]
            }
            for doc in retrieved_docs
        ]
    )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    parsed_data = symptom_parser.extract_symptoms(request.message)

    current_session = chat_memory.get_session(request.session_id)

    follow_up_result = follow_up_interpreter.interpret(
        user_message=request.message,
        last_question=current_session.get("last_follow_up_question")
    )

    parsed_data["symptoms"].extend(follow_up_result["extra_symptoms"])

    chat_memory.add_message(
        session_id=request.session_id,
        role="user",
        content=request.message
    )

    chat_memory.update_medical_context(
        session_id=request.session_id,
        symptoms=parsed_data["symptoms"],
        severity=parsed_data["severity"],
        duration=parsed_data["duration"]
    )

    progression_factors = progression_interpreter.interpret(
        user_message=request.message,
        severity=parsed_data["severity"],
        duration=parsed_data["duration"]
    )

    for factor in progression_factors:
        chat_memory.add_progression_factor(
            session_id=request.session_id,
            factor=factor
        )

    chat_memory.add_risk_factors(
        session_id=request.session_id,
        risk_factors=follow_up_result["risk_factors"]
    )

    session = chat_memory.get_session(request.session_id)

    symptoms = session["symptoms"]
    severity = session["severity"]
    duration = session["duration"]
    risk_factors = session["risk_factors"]
    latest_risk_factors = session["latest_risk_factors"]
    progression_factors = session["progression_factors"]

    urgency = urgency_engine.calculate_urgency(
        symptoms=symptoms,
        severity=severity,
        risk_factors=risk_factors,
        progression_factors=progression_factors
    )

    retrieved_docs = medical_knowledge_service.get_sources(symptoms)
    explanation = medical_knowledge_service.build_explanation_with_context(
        symptoms=symptoms,
        risk_factors=risk_factors
    )
    turn_insight = conversation_reasoner.generate_turn_insight(
        symptoms=symptoms,
        risk_factors=risk_factors,
        latest_risk_factors=latest_risk_factors
    )
    progression_insight = conversation_reasoner.generate_progression_insight(
        progression_factors=progression_factors
    )

    if progression_insight:
        explanation = progression_insight

    if turn_insight:
        explanation = turn_insight

    explanation = response_safety.clean_response(
        response=explanation,
        symptoms=symptoms,
        retrieved_docs=retrieved_docs
    )

    asked_questions = chat_memory.get_asked_questions(request.session_id)

    follow_up_question = medical_knowledge_service.get_follow_up_question(
        symptoms=symptoms,
        asked_questions=asked_questions
    )

    chat_memory.set_last_follow_up_question(
        session_id=request.session_id,
        question=follow_up_question
    )

    chat_memory.add_asked_question(
        session_id=request.session_id,
        question=follow_up_question
    )
    if case_summary_builder.should_generate_summary(
            asked_questions=asked_questions,
            symptoms=symptoms,
            severity=severity,
            duration=duration
    ):
        final_reply = case_summary_builder.build_summary(
            symptoms=symptoms,
            severity=severity,
            duration=duration,
            urgency=urgency,
            risk_factors=risk_factors,
            progression_factors=progression_factors
        )

        follow_up_question = None
    else:
        final_reply = chat_response_builder.build_reply(
            explanation=explanation,
            urgency=urgency,
            follow_up_question=follow_up_question,
            risk_factors=risk_factors,
            progression_factors=progression_factors
        )


    chat_memory.add_message(
        session_id=request.session_id,
        role="assistant",
        content=final_reply
    )

    return ChatResponse(
        session_id=request.session_id,
        symptoms=symptoms,
        severity=severity,
        duration=duration,
        urgency=urgency,
        reply=final_reply,
        follow_up_question=follow_up_question,
        disclaimer=DISCLAIMER,
        sources=[
            {
                "id": doc["id"],
                "title": doc["title"],
                "source": doc["source"]
            }
            for doc in retrieved_docs
        ]
    )


@app.delete("/chat/{session_id}")
def clear_chat_session(session_id: str):
    chat_memory.delete_session(session_id)

    return {
        "message": f"Session '{session_id}' cleared successfully."
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "MedGuide AI"
    }