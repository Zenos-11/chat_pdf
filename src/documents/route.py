from fastapi import APIRouter, UploadFile, File, Depends
from src.documents import service
from src.auth.dependencies import get_current_user
from src.chat.enging import rag_engine

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile= File(...),
                     current_user: dict = Depends(get_current_user)):
    return await service.process_pdf(file, username=current_user["username"])

@router.get("/count")
async def doc_count(current_user: dict = Depends(get_current_user)):
    """返回当前用户在向量库中的文档片段数量"""
    try:
        res = rag_engine.vector_db._collection.get(where={"owner": current_user["username"]})
        count = len(res.get("ids", []))
        return {"owner": current_user["username"], "chunks": count}
    except Exception as e:
        return {"owner": current_user["username"], "error": str(e)}