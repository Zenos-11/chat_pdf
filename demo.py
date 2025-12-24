import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from openai import OpenAI

DEEPSEEK_KEY = "sk-4d6e671585284c19b12a2fa9eba546b3"
BASE_URL = "https://api.deepseek.com"

raw_texts = [
    "DeepSeek-V3 是一个强大的混合专家 (MoE) 语言模型，总参数量为 671B。",
    "Docker 的 -p 参数用于端口映射，格式为 宿主机端口:容器端口。",
    "小明的秘密：他表面上是程序员，实际上是国家一级面点师，最擅长做流沙包。",
]
documents = [Document(page_content=text) for text in raw_texts]

print("<<< 1. init")
embeddings = HuggingFaceEmbeddings(model_name = "moka-ai/m3e-base")


print("<<< 2. vectorize")
db = Chroma.from_documents(documents, embeddings)

print("<<< 3. question")
query = "用四个字回答我，Docker 的 -p 参数是干什么用的？"

print("<<< 4. searching")
results = db.similarity_search(query, k=1)
retrieve = results[0].page_content
print(f"find something similar： {retrieve}")

print("<<< 5. ask llm")
prompt = f"""
你是一个聪明的助手。请根据下面的【参考资料】回答用户的【问题】。
如果你在资料里找不到答案，就诚实地说不知道，不要瞎编

【参考资料】
{retrieve}

【问题】
{query}
"""

print("<<< 6. send msg to LLM")
client = OpenAI(api_key=DEEPSEEK_KEY, base_url=BASE_URL)
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个基于知识库的问答助手"},
        {"role": "user", "content": prompt}],
    temperature= 0.1
)
print("<<< 7. response from LLM")
print(response.choices[0].message.content)