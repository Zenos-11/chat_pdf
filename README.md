# ChatPdf

> Summrize your pdf file.

1. 首先把文档向量化存储在数据库
2. 然后根据问题搜索数据库，找出关联最大的句子
3. 最后调用 api，以关联最大的句子为参考信息，让 ai 从参考信息中找出问题的最优回答

经过以上步骤，能得到大致的问题答案
##📝A useful artical searcher
It reads your pdf files, and digest all it recognized

> you may ask
> what is the main idea of this artical?
> it will summerize this pdf file
