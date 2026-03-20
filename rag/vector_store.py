from langchain_chroma import Chroma
from ..utils.config_handler import chroma_config
from ..model.factory import embed_model,chat_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from ..utils.logger_handler import logger
from ..utils.path_tool import get_abs_path
from ..utils.file_handler import txtloader,pdfloader,listdir_with_allowed_type,get_file_md5_hex

class VectorStoreService:
    def __init__(self):
        self.vector_store=Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_config['persist_directory'],
        )

        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=chroma_config['chunk_size'],
            chunk_overlap=chroma_config['chunk_overlap'],
            separators=chroma_config['separators'],
            length_function= len
        )


    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k":chroma_config['k']})
    def load_document(self):
        def check_md5hex(md5forcheck:str):
            if not os.path.exists(get_abs_path(chroma_config['md5_hex_store'])):
                open(get_abs_path(chroma_config['md5_hex_store']), 'w',encoding="utf-8").close()
                return False

            with open(get_abs_path(chroma_config['md5_hex_store']), 'r',encoding="utf-8") as f:
                for line in f.readlines():
                    line=line.strip()
                    if line ==md5forcheck:
                        return True

                return False

        def savemd5_hex(md5forcheck:str):
            with open(get_abs_path(chroma_config['md5_hex_store']), 'a',encoding="utf-8") as f:
                f.write(md5forcheck+"\n")
        def get_file_documents(readpath:str):
            if readpath.endswith('.txt'):
                return txtloader(readpath)
            if readpath.endswith('.pdf'):
                return pdfloader(readpath)
            return []
        allowed_file_path:list[str]=listdir_with_allowed_type(
            get_abs_path(chroma_config['data_path']),
            tuple(chroma_config["allow_knowledge_file_type"])
        )

        for path in allowed_file_path:
            md5_hex=get_file_md5_hex(path)
            if check_md5hex(md5_hex):
                logger.info(f"[记载知识库]{path}已存在，跳过")
                continue
            try:
                documents:list[Document]=get_file_documents(path)

                if not documents:
                    logger.error(f"[加载知识库]，{path}无内容")
                    continue

                self_document=self.spliter.split_documents(documents)
                if not self_document:
                    logger.error(f"[加载知识库]{path}分片后，没有有效内容")
                    continue
                self.vector_store.add_documents(self_document)
                savemd5_hex(md5_hex)

                logger.info(f"[加载知识库]{path}加载成功")
            except Exception as e:
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}",exc_info=True)

if __name__ == '__main__':
    vs=VectorStoreService()
    vs.load_document()
    retriver=vs.get_retriever()

    res=retriver.invoke("迷路")
    print(res)
    print("halo")
    for r in res:
        print(r.page_content)
        print("-"*40)
