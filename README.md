# MedGuide AI

AI-powered conversational medical triage assistant built with FastAPI and Next.js. The system guides users through symptom discussions using multi-turn conversations, dynamic follow-up questions, urgency assessment, symptom reasoning, and case summarization while remaining educational and non-diagnostic.

## Features

### Conversational Symptom Assessment

* Multi-turn medical conversations
* Session-based memory
* Dynamic symptom extraction
* Context-aware follow-up questions
* Progressive symptom refinement

### Medical Reasoning Engine

* Symptom normalization and mapping
* Medical knowledge base integration
* Risk factor identification
* Progression tracking
* Severity assessment
* Duration analysis

### Triage and Urgency Assessment

* LOW urgency
* MODERATE urgency
* HIGH urgency
* EMERGENCY urgency

### Case Summarization

* Symptom summary
* Severity summary
* Duration summary
* Risk factor summary
* Progression summary
* Final recommendation

### Safety Layer

* Educational use only
* No medical diagnosis
* No treatment recommendations
* Clear medical disclaimer
* Emergency escalation for red-flag symptoms

---

## Architecture

### Backend

FastAPI-based architecture:

```text
User Input
    ↓
Symptom Parser
    ↓
Chat Memory
    ↓
Follow-up Interpreter
    ↓
Progression Interpreter
    ↓
Medical Knowledge Service
    ↓
Conversation Reasoner
    ↓
Urgency Engine
    ↓
Response Safety Layer
    ↓
Chat Response Builder
    ↓
Case Summary Builder
    ↓
API Response
```

### Frontend

Built with:

* Next.js
* React
* TypeScript
* Tailwind CSS

Frontend features:

* Real-time chat interface
* Auto-scroll conversation view
* Urgency badges
* Source display
* Session management
* New Chat functionality
* Responsive design

---

## Project Structure

```text
MedGuide-AI/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   │
│   │   ├── services/
│   │   │   ├── symptom_parser.py
│   │   │   ├── urgency_engine.py
│   │   │   ├── chat_memory.py
│   │   │   ├── follow_up_interpreter.py
│   │   │   ├── progression_interpreter.py
│   │   │   ├── medical_knowledge_service.py
│   │   │   ├── conversation_reasoner.py
│   │   │   ├── response_safety.py
│   │   │   ├── chat_response_builder.py
│   │   │   ├── case_summary_builder.py
│   │   │   └── ai_response_generator.py
│   │   │
│   │   └── data/
│   │       └── medical_knowledge.json
│   │
│   └── requirements
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── globals.css
│   │
│   ├── package.json
│   └── next.config.ts
│
└── README.md
```

---

## Technology Stack

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

### AI Components

* Symptom Extraction
* Medical Knowledge Base
* Conversation Memory
* Medical Reasoning Engine
* Dynamic Follow-Up Generation
* Triage Assessment

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/JabranMustafa/MedGuide-AI.git
cd MedGuide-AI
```

### Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements

python -m uvicorn app.main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```text
http://localhost:3000
```

---

## Example Conversation

User:

```text
I have pain in my back
```

Assistant:

```text
Possible explanation:
Back pain can be related to muscle strain, poor posture, heavy lifting, disc irritation, nerve irritation, kidney-related problems.

Urgency level:
LOW

Follow-up question:
Does the pain go down your leg?
```

User:

```text
Yes
```

Assistant:

```text
Possible explanation:
Pain going down the leg can sometimes happen when a nerve in the lower back is irritated or compressed.

Urgency level:
MODERATE

Follow-up question:
Do you have numbness or weakness?
```

---

## Disclaimer

This project is intended for educational and demonstration purposes only.

It does not provide medical diagnoses, treatment recommendations, or professional medical advice.

Users should consult qualified healthcare professionals for any medical concerns.

---

## Future Improvements

* Database persistence
* User authentication
* Clinical guideline integration
* Multi-language support
* Retrieval-Augmented Generation (RAG)
* Cloud deployment
* Analytics dashboard
* Voice interaction
* Medical document upload
* Integration with trusted medical sources

---

## License

MIT License
