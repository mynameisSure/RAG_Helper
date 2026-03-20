from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from agent.model.factory import chat_model
from agent.rag.vector_store import VectorStoreService
from agent.utils.prompt_loader import load_rag_prompt


class RagSummarizeService(object):
    def __init__(self):
        self.vector_store=VectorStoreService()
        self.retriever=self.vector_store.get_retriever()
        self.prompt_text=load_rag_prompt()
        self.prompt_template=PromptTemplate.from_template(self.prompt_text)
        self.model=chat_model
        self.chain=self._init_chain()

    def printtemplate(self,template):
        print(f"{'=='*20}\n{template}\n{'=='*20}\n")
        return template
    def _init_chain(self):
        chain=self.prompt_template |self.printtemplate|self.model|StrOutputParser()
        return chain

    def retriever_docs(self,query)->list[Document]:
        return self.retriever.invoke(query)
    def rag_summarize(self,query):
        context_doc=self.retriever_docs(query)
        count=0
        context=""
        for doc in context_doc:
            count+=1
            context+=f"【参考资料{count}】：{doc.page_content}|参考元数据：{doc.metadata}\n"

        return self.chain.invoke(
            {
                "input":query,
                "context":context,
            }
        )

if __name__ == '__main__':
    rag=RagSummarizeService()
    res=rag.rag_summarize("小户型适合哪些机器人？")
    print(res)
