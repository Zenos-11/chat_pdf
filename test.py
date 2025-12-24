import os
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document 

raw_text = [
    "Docker 是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的镜像中。",
    "FastAPI 是一个用于构建 API 的现代、快速（高性能）的 Web 框架，基于标准 Python 类型提示。",
    "RAG (检索增强生成) 是一种技术，它通过从外部知识库检索相关信息来增强大语言模型的能力。",
    "小明今天早上吃了两个包子，感觉非常饱。",  # 这是一条干扰数据
]

documemts = [Document(page_content=text) for text in raw_text]

print(">>> 1.init")
embeddings = HuggingFaceEmbeddings(model_name = "moka-ai/m3e-base")


print(">>> 2.vectorize")
db = Chroma.from_documents(documemts, embeddings)

print(">>> 3. question")
query = "小红喜欢是什么？"

print(">>> 4. searching")
results = db.similarity_search(query, k=1)

print("\n>>> 5. results")
for doc in results:
    print("----------------------")
    print(f"原文内容:{doc.page_content}")