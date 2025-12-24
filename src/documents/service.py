import io
from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.chat.enging import rag_engine

async def process_pdf(file: UploadFile):
    """
    接收pdf--提取文字--切片--存入向量库
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="only pdf supported")
    try:
        # 读取内容
        content = await file.read()
        pdf_file = io.BytesIO(content)
        reader = PdfReader(pdf_file)

        #提取文字
        raw_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text + "\n"

        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="PDF 中未检测到可提取文本")
            # chunking 切片
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "！", "，"]
        )
        chunks = text_splitter.split_text(raw_text)
        print(f">>> [Document Service]解析完成，一共切{len(chunks)}个片段")

        rag_engine.vector_db.add_texts(chunks)
        rag_engine.vector_db.persist()
        return{
            "filename": file.filename,
            "total_pages": len(reader.pages),
            "chunks_created":len(chunks)
        }
    
    except Exception as e:
        print("解析pdf失败")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
