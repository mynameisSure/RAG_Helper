import os

from langchain_core.tools import tool
from ..rag.rag_service import RagSummarizeService
import random
from ..utils.config_handler import agent_config
from uapi import UapiClient
from uapi.errors import UapiError
from ..utils.logger_handler import logger
from ..utils.path_tool import get_abs_path
client = UapiClient("https://uapis.cn", token=agent_config["weather_api_key"])
rag=RagSummarizeService()
user_ids=["1001","1002","1003","1004","1005","1006","1007","1008","1009","1010"]
mouth=["2025-01","2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10","2025-11","2025-12"]
@tool(description="从向量知识库中检索资料")
def rag_summarize(query):
    return rag.rag_summarize(query)

@tool(description="获取指定city的天气，输入city的字符串，获取天气,例如：{'city':'北京'}")
def get_weather(city:str):
    city=city.strip()
    try:
        result=client.misc.get_misc_weather(city=city,extended=True)
        return result
    except UapiError as e:
        logger.error(e)
        return str(e)
@tool(description="获取用户所在的城市位置")
def get_user_location():
    try:
        result=client.network.get_network_myip(source="commercial")
        return result
    except UapiError as e:
        return str(e)

@tool(description="获取用户id")
def get_user_id():
    return random.choice(user_ids)
@tool(description="获取当前月份")
def get_current_month():
    return random.choice(mouth)
external_data={}
def generate_external_data():
    if not external_data:
        external_data_path=get_abs_path(agent_config["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError("外部数据不存在")

        with open(external_data_path,"r",encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr:list[str]=line.strip().split(",")
                user_id:str=arr[0].replace('"','').strip()
                feature=arr[1].replace('"','').strip()
                efficiency=arr[2].replace('"','').strip()
                consumables=arr[3].replace('"','').strip()
                comparison=arr[4].replace('"','').strip()
                time=arr[5].replace('"','').strip()
                if user_id not in external_data:
                    external_data[user_id]={}
                external_data[user_id][time]={
                    "特征":feature,
                    "效率":efficiency,
                    "耗材":consumables,
                    "对比":comparison,

                }
@tool(description="从外部系统钟获取指定用户在指定月份的使用记录，以纯字符串的形式返回,没有则返回空字符串")
def fetch_external_data(user_id:str,mouth:str):
    generate_external_data()
    try:
        return external_data[user_id][mouth]
    except KeyError:
        logger.error(f"{fetch_external_data}未能检索到用户{user_id}在{mouth}使用记录")
        return ""

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息。为后续提示词切换上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"