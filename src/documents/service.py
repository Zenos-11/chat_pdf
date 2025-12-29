# src/documents/service.py
import os
from tempfile import NamedTemporaryFile
from markitdown import MarkItDown
from fastapi import UploadFile, HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.chat.enging import rag_engine


md = MarkItDown()


async def process_pdf(file: UploadFile, username: str):
    """将 PDF 转为 Markdown，切片后写入向量库，并返回统计信息"""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="only pdf supported")

    # MarkItDown 需要本地文件路径
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        temp_path = tmp.name
        tmp.write(await file.read())

    try:
        # 1) PDF -> Markdown
        result = md.convert(temp_path)
        markdown_text = (result.text_content or "").strip()
        if not markdown_text:
            raise HTTPException(status_code=400, detail="PDF 提取内容为空")

        # 2) 切片
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            separators=["\n\n", "\n", "。", "！", "？", "##", "#"],
        )
        chunks = splitter.split_text(markdown_text)
        if not chunks:
            raise HTTPException(status_code=400, detail="切片结果为空")

        # 3) 入向量库（带 metadata）
        documents = [
            Document(page_content=chunk, metadata={"owner": username, "source": file.filename})
            for chunk in chunks
        ]
        ids = rag_engine.vector_db.add_documents(documents)

        # Chroma 0.4+ 自动持久化，这里保留调用兼容旧版本
        try:
            rag_engine.vector_db.persist()
        except Exception:
            pass

        # 4) 统计
        owner_chunks = None
        try:
            stats = rag_engine.vector_db._collection.get(where={"owner": username})
            owner_chunks = len(stats.get("ids", []))
        except Exception:
            pass

        return {
            "filename": file.filename,
            "owner": username,
            "chunks_created": len(chunks),
            "ids": ids,
            "owner_chunks": owner_chunks,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)