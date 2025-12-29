from fastapi import APIRouter, Depends
from src.chat.enging import rag_engine
from src.chat.schemas import ChatRequest
from src.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/ask")
async def ask_questions(request:ChatRequest, current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    answer = rag_engine.search_and_answer(request.question, username, request.context)
    return {"answer": answer}