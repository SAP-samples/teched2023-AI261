# simple-agent-teched
Simple implementation of Reason &amp; Act agent without langchain

<img width="400" alt="image" src="https://github.com/SAP-samples/teched2023-AI261/blob/main/exercises/ex5/images/ai_agent_diagram.png">

# Prerequisites
1. Python (3.10.11) & pip installed
3. Git installed
2. key.json file containing LLM access key inside the secrets folder

# Initial setup
Feel free to skip if done
1. Install Python (3.10.11): https://www.python.org/downloads/release/python-31011/. Note: For Python 3.4 or later, pip is included by default
2. Install git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
3. Visual Studio Code for editing code: https://code.visualstudio.com/download 

# How to use
1. Open Desktop > Session Materials Github > AI261. This is a shortcut that open the github repo teched2023-AI261
2. Please download the repo as a .zip file by clicking on the green button 'Code'
3. Unzip the downloaded .zip file (teched2023-AI261-main) and open it on Visual Studio Code or an editor of your choice
4. Open the terminal (either inside the editor or as command prompt) and navigate to `teched2023-AI261/exercises/ex5/`
5. create python virutal environment `python -m venv ./venv`
6. activate the virtual environment, on Windows `.\venv\Scripts\activate` or on Mac `source venv/bin/activate`
7. run `pip install -r requirements.txt` to install required python packages
8. run the agent `streamlit run app.py`
9. start typing and enjoy!

# What can the agent do?
1. Have a conversation with you similar to chatGPT
2. Use tools, for details check the tools.yaml file

# Why is that useful?
1. Ask chatGPT what the factorial of 143 is, then ask your agent the same :sunglasses:

# How can I add a tool?
1. Add tool name, description and example to tools.yaml
2. create xyz_tool.py file, for how to do that, check out factorial_tool.py
3. integrate tool into the toolkit file tools.py (import it and add it to the toolkit)

