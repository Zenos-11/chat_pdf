from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from openai import OpenAI
from src.config import settings

class RAGEnging:
    #加载向量模型
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
    
    #连接向量数据库
        self.vector_db = Chroma(
            persist_directory=settings.CHROMA_DB_PATH,
            embedding_function=self.embeddings
        )    
    
    #初始化ai客户端
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )

    def search_and_answer(self, question: str, manual_context: list[str] | None = None):
        manual_context = manual_context or []
        docs = self.vector_db.similarity_search(question, k=3)
        retrieved_context = [d.page_content for d in docs]
        merged_context = retrieved_context + manual_context
        if not merged_context:
            return "知识库暂无可用内容，请先上传包含相关信息的文档。"

        context = "\n".join(merged_context)
        prompt = f"""【知识库内容】
        你是一个聪明的助手。请根据下面的【参考资料】回答用户的【问题】。
        如果你在资料里找不到答案，就诚实地说不知道，不要瞎编
        【参考资料】
        {context}

        【问题】
        {question}
        """
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "你是一个专业的中文知识库问答助手。"},
                      {"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return "ai回答："+response.choices[0].message.content.strip()
        
    
rag_engine = RAGEnging()