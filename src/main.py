from fastapi import FastAPI
from src.chat.router import router as chat_router
from src.documents.route import router as doc_router
from src.auth.router import router as auth_router
app = FastAPI(title = "专业RAG知识库")

app.include_router(chat_router, prefix="/api/v1/chat", tags=["对话"])
app.include_router(doc_router, prefix="/api/v1/docs", tags=["文档管理"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["用户认证"])

@app.get("/")
async def root():
    return {"status": "ok","message":"AI RAG已就绪"}
