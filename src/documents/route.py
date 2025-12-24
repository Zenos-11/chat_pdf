from fastapi import APIRouter, UploadFile, File
from src.documents import service

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile= File(...)):
    return await service.process_pdf(file)