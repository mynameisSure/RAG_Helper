import streamlit as st
import sys
from pathlib import Path
import time

from .react_agent import ReactAgent

st.title("智扫通机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()
if "message"not in st.session_state:
    st.session_state["message"] = []
print(st.session_state["message"])


for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])
prompt=st.chat_input("输入消息...")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})
    response_message=[]
    with st.spinner("智能客服思考中......"):
        res=st.session_state["agent"].excute_stream(prompt)
        def capture(generator,cache_list):
            for i, chunk in enumerate(generator):
                if i == 0:
                    continue
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res,response_message))
        st.session_state["message"].append({"role":"assistant","content":response_message[-1]})
        st.rerun()