# ChatPdf

> Summrize your pdf file.

## 过程
1. 首先把文档向量化存储在数据库
2. 然后根据问题搜索数据库，找出关联最大的句子
3. 最后调用 api，以关联最大的句子为参考信息，让 ai 从参考信息中找出问题的最优回答

## Process
1. First, vectorize the documents and store them in a database
2. Then, search the database based on the question to find the most relevant sentences
3. Finally, call the API, using the most relevant sentences as reference information, and have the AI find the optimal answer to the question from the reference information



