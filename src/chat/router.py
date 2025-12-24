from fastapi import APIRouter
from src.chat.enging import rag_engine
from src.chat.schemas import ChatRequest

router = APIRouter()

@router.post("/ask")
async def ask_questions(request:ChatRequest):
    answer = rag_engine.search_and_answer(request.question, request.context)
    return {"answer": answer}