import json
import os

import googlesearch
import requests
from bs4 import BeautifulSoup
from tools.base_tool import BaseTool

DIR = os.path.dirname(os.path.abspath(__file__))
N_URLS = 3
REQUEST_TIMEOUT = 30
MAX_RESULT_LENGTH = 500

class WebSearchTool(BaseTool):

    @property
    def name(self):
        return "web_search"

    def action(self, action_input: str):
        input_json = json.loads(str(action_input).replace("'", '"'), strict=False)
        query = input_json.get("query")
        urls = input_json.get("urls")
        text_content, citations = self.web_search(query=query, urls=urls)
        citations_text = ", ".join(citations)

        observation = text_content + "\n" + "Citations: " + citations_text
        return {"Observation": observation}


    def web_search(self, query, urls=None):
        content = "Web Search did not work."
        citations = []
        try:
            if urls == None:
                search_results = googlesearch.search(query, lang="en")
                urls = list(search_results)
                urls = urls[:N_URLS]
                citations = urls
            text_chunks = []
            for url in urls:
                response = requests.get(url, timeout=REQUEST_TIMEOUT)
                soup = BeautifulSoup(response.content, "html.parser")
                irrelevant_classes_ids = ["header","nav","nav-bar","contacts","footer","menu","topbar","navigation","links",]
                for class_name in irrelevant_classes_ids:
                    elements = soup.find_all(class_=class_name)
                    for element in elements:
                        element.extract()
                for id_name in irrelevant_classes_ids:
                    element = soup.find(id=id_name)
                    if element:
                        element.extract()
                relevant_data = soup.find_all("p")
                text_content = ""
                for data in relevant_data:
                    text_content = text_content + data.get_text()
                text_content = (text_content.replace("\t", " ")).replace("\xa0", " ")
                text_content = text_content.strip()
                text_chunks.append(text_content)
            content = "\n".join(text_chunks)
        except Exception as e:
            content = f"Error encountered: {e}"
            citations = []

        return f"Web Content: {content[:MAX_RESULT_LENGTH]}", citations
