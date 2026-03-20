from abc import ABC,abstractmethod
from typing import Optional

from langchain_community.embeddings import DashScopeEmbeddings
from ..utils.config_handler import rag_config
from langchain_community.chat_models import ChatTongyi
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self)->Optional[Embeddings |BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self)->Optional[Embeddings |BaseChatModel]:
        return ChatTongyi(model=rag_config['chat_model_name'],api_key=rag_config['api'])

class EmbedModelFactory(BaseModelFactory):
    def generator(self)->Optional[Embeddings |BaseChatModel]:
        return DashScopeEmbeddings(model=rag_config['embedding_model_name'],dashscope_api_key=rag_config['api'])


embed_model=EmbedModelFactory().generator()
chat_model=ChatModelFactory().generator()
