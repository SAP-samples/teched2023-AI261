import json
from math import factorial

from tools.base_tool import BaseTool


class FactorialTool(BaseTool):
    @property
    def name(self):
        return "calculate_factorial"


    def action(self, action_input: str):
        input_json = json.loads(str(action_input).replace("'", '"'), strict=False)
        return factorial(input_json["number"])
