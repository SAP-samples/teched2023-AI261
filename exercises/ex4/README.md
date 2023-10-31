# simple-agent-teched
Simple implementation of Reason &amp; Act agent without langchain for Teched

# Prerequisites
1. Python (3.10.11) & pip installed
2. key.json file containing LLM access key inside the secrets folder

# How to use
1. open command line project root folder
2. create python virutal environment `python -m venv ./venv`
3. activate the virtual environment, on Windows `.\venv\Scripts\activate` or on Mac `source venv/bin/activate`
4. Navigate to [exercises/ex4/](exercises/ex4/)
5. run `pip install -r requirements.txt` to install required python packages
6. run the agent `streamlit run app.py`
7. start typing and enjoy!

# What can the agent do?
1. Have a conversation with you similar to chatGPT
2. Use tools, for details check the tools.yaml file

# Why is that useful?
1. Ask chatGPT what the factorial of 143 is, then ask your agent the same :sunglasses:

# How can I add a tool?
1. Add tool name, description and example to tools.yaml
2. create xyz_tool.py file, for how to do that, check out factorial_tool.py
3. integrate tool into the toolkit file tools.py (import it and add it to the toolkit)

