from langchain.agents import create_agent
from .model.factory import chat_model
from .utils.prompt_loader import load_system_prompt
from .tools.agent_tools import get_weather, get_user_id, get_current_month, get_user_location, rag_summarize, \
    fill_context_for_report, fetch_external_data
from .tools.middleware import monitor_tool, log_before_model, report_prompt_switch


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize, get_weather, get_current_month, get_user_location, fetch_external_data,
                   fill_context_for_report, get_user_id],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )

    def excute_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query},
            ]
        }
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            lastmessage = chunk["messages"][-1]
            if lastmessage:
                yield lastmessage.content.strip() + "\n"


if __name__ == '__main__':

    agent = ReactAgent()
    for chunk in agent.excute_stream("总结一下我的使用情况"):
        print(chunk, end="", flush=True)
