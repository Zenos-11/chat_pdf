import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from openai import OpenAI  # 我们用 OpenAI 的库来调用 DeepSeek（它们兼容）

# ================= 配置区域 =================
# 替换成你的 DeepSeek API Key
DEEP_SEEK_API_KEY = "sk-4d6e671585284c19b12a2fa9eba546b3"
BASE_URL = "https://api.deepseek.com"  # DeepSeek 的官方地址

# ================= 1. 准备工作 (图书管理员) =================
print(">>> 1. [管理员] 正在初始化本地向量模型...")
embeddings = HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")

# 模拟知识库数据 (真实场景下这里是读 PDF)
raw_texts = [
    "DeepSeek-V3 是一个强大的混合专家 (MoE) 语言模型，总参数量为 671B。",
    "Docker 的 -p 参数用于端口映射，格式为 宿主机端口:容器端口。",
    "小明的秘密：他表面上是程序员，实际上是国家一级面点师，最擅长做流沙包。",
]
documents = [Document(page_content=text) for text in raw_texts]

print(">>> 2. [管理员] 正在将数据存入向量库...")
# 创建一个临时的内存数据库
db = Chroma.from_documents(documents, embeddings)

# ================= 2. 用户提问 =================
user_query = "小明的真实身份是什么？"
print(f"\n>>> 用户提问: {user_query}")

# ================= 3. 检索 (找最像) =================
print(">>> 3. [管理员] 正在去书架上找资料...")
# 找最相关的 1 条信息
results = db.similarity_search(user_query, k=1)
retrieved_text = results[0].page_content

print(f"    -> 找到了这条资料: 「{retrieved_text}」")
print("    -> (此时还没有逻辑，只是把字找出来了)")

# ================= 4. 组装 (关键步骤！) =================
# 这就是 RAG 的魔法：把“问题”和“资料”拼在一起，骗 AI 说这是它自己知道的
prompt = f"""
你是一个聪明的助手。请根据下面的【参考资料】回答用户的【问题】。
如果你在资料里找不到答案，就诚实地说不知道，不要瞎编。

【参考资料】：
{retrieved_text}

【问题】：
{user_query}
"""

print("\n>>> 4. [系统] 正在把资料和问题打包发给 DeepSeek (老教授)...")

# ================= 5. 推理 (老教授发挥逻辑) =================
client = OpenAI(api_key=DEEP_SEEK_API_KEY, base_url=BASE_URL)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个基于知识库的问答助手。"},
        {"role": "user", "content": prompt},
    ],
    temperature=0.1,  # 温度设低点，让它严谨一点
)

answer = response.choices[0].message.content

print("\n" + "="*30)
print(f"🤖 DeepSeek 的回答:\n{answer}")
print("="*30)