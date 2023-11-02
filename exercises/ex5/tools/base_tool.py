from abc import ABC, abstractmethod

"""Base template for tool that a LLM can interact with.
- 'name' is a short string with which the llm can call the tool, will be part of the prompt, also key of the dict for the agent to call the action
- 'action' is the python function that will be called if the llm wants to use the tool,
action_input will also be defined by llm"""


class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def action(self, action_input: str):
        pass
