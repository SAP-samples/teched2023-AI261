import os

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL_PROMPT_FILE = os.path.join(HERE, "tools.yaml")
AGENT_PROMPT_FILE = os.path.join(HERE, "agent.yaml")


def get_agent_system_message(tool_list: list) -> str:
    available_actions = "Available Actions:\n"
    for tool in tool_list:
        available_actions += f"{tool}:\n{_load_tool_prompt(tool)}\n-----\n"
    agent_prompt = _load_prompt(AGENT_PROMPT_FILE)

    return f"""{agent_prompt["instructions"]}

{agent_prompt["output_format"]}

{available_actions}
"""

def _load_prompt(file_path: str):
    data = None
    with open(file_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(str(e))
    return data


def _load_tool_prompt(tool_name: str):
    data = {}
    with open(TOOL_PROMPT_FILE, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(str(e))
    tool_prompt = data.get(tool_name)

    if tool_prompt is not None:
        return tool_prompt
    else:
        print(f"Tool prompt for {tool_name} does not exist!")
        return ""
