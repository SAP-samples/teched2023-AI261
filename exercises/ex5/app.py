import json

import streamlit as st
from agent import Agent
from clients import GPTClient
from tools.tools import create_tools

llm_config = {
    "DEPLOYMENT_ID": "gpt-4-32k",
    "MAX_TOKENS": 3000,
    "TEMPERATURE": 0.1
}

llm_key = {}
with open("./secrets/key.json", "r") as f:
    llm_key = json.load(f)

# Create LLM Client
llm_client = GPTClient(svc_key=llm_key, llm_config=llm_config)

# Create Agent Toolkit
toolkit = create_tools()

# Create AI Agent
agent_config = {
    "RETRY_TIMEOUT": 60,
    "HISTORY_LENGTH": 32,
    "MAX_ITERATIONS": 5,
    "MAX_RETRIES": 3,
    "RECORD": 1
}

_agent = Agent(toolkit=toolkit, llm_client=llm_client, agent_config=agent_config)


# App title
st.set_page_config(page_title="🤗 HiAgentt")

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLM response
def start_agent_run(prompt_input):
    return _agent.ask_gpt(streamlit=st, user_input=prompt_input)

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start_agent_run(prompt)
