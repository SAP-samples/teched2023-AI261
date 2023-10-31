from tools.web_search_tool import WebSearchTool
from tools.factorial_tool import FactorialTool

############################# Toolkit #############################
def create_tools() -> dict:
    web_search = WebSearchTool()
    factorial = FactorialTool()

    toolkit = {
        web_search.name: web_search.action,
        factorial.name: factorial.action
    }

    return toolkit
