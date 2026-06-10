import random
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])

GREETINGS = [
    "Welcome to Biocraft Digital. How may I assist you today?",
    "Greetings. I am the Biocraft assistant. What can I help you with?",
    "Hello. I'm online and ready to assist.",
]

FAQ = [
    {
        "keywords": ["service", "offer", "do you do", "capabilities"],
        "answer": "Biocraft Digital specializes in three core areas:\n\n"
        "• Custom Software — bespoke platforms tailored to your operations\n"
        "• Cloud Infrastructure — edge & serverless architectures\n"
        "• AI Integration — machine learning and cognitive computing\n\n"
        "Which area interests you?",
    },
    {
        "keywords": ["price", "cost", "pricing", "budget", "how much"],
        "answer": "Our pricing is project-based and depends on scope and complexity. "
        "We offer solutions from $5k to $50k+. "
        "Contact our team for a tailored quote.",
    },
    {
        "keywords": ["timeline", "how long", "delivery", "when"],
        "answer": "Typical project timelines range from 1 to 6 months depending on scope. "
        "We'll provide a detailed timeline during the proposal phase.",
    },
    {
        "keywords": ["contact", "reach", "email", "talk", "human"],
        "answer": "You can reach our team through the contact form on this page, "
        "or create an account to submit a project inquiry directly.",
    },
    {
        "keywords": ["tech", "stack", "technology", "python", "react", "fastapi"],
        "answer": "We work with modern stacks: Python/FastAPI, React/Next.js, "
        "PostgreSQL, cloud-native architectures, and AI/ML pipelines.",
    },
]


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


def classify_intent(message: str):
    msg = message.lower().strip()

    greetings = ["hello", "hi ", "hey", "greetings", "good morning", "good evening"]
    if any(msg.startswith(g) or msg == g.strip() for g in greetings):
        return "greeting"

    for faq in FAQ:
        if any(kw in msg for kw in faq["keywords"]):
            return faq["answer"]

    return None


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = classify_intent(request.message)

    if result == "greeting":
        return ChatResponse(reply=random.choice(GREETINGS))

    if result:
        return ChatResponse(reply=result)

    return ChatResponse(
        reply="Thank you for your message. "
        "For specific inquiries, please create an account and submit a project request. "
        "Our team typically responds within 24 hours.\n\n"
        "In the meantime, feel free to ask about our services, pricing, or process."
    )
