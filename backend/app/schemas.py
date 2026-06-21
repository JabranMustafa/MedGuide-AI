from pydantic import BaseModel
from typing import List, Optional


class SymptomRequest(BaseModel):
    message: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


class RetrievedDocument(BaseModel):
    id: str
    title: str
    source: str


class SymptomResponse(BaseModel):
    symptoms: List[str]
    severity: Optional[str]
    duration: Optional[str]
    urgency: str
    explanation: str
    disclaimer: str
    sources: List[RetrievedDocument]


class ChatResponse(BaseModel):
    session_id: str
    symptoms: List[str]
    severity: Optional[str]
    duration: Optional[str]
    urgency: str
    reply: str
    follow_up_question: Optional[str]
    disclaimer: str
    sources: List[RetrievedDocument]