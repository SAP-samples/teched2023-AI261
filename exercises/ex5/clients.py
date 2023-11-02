import json
from datetime import datetime, timedelta, timezone

import requests

REQUEST_TIMEOUT = 30
TOKEN_EXPIRY = 5

class GPTClient:
    """Interface to the LLM provider API"""

    def __init__(self, svc_key, llm_config) -> None:
        if svc_key is None or llm_config is None:
            raise Exception(
                "LLM Service client is incorrectly configured; check the environment credentials or configuration is passed"
            )
        self.uaa_client_id = svc_key["uaa"]["clientid"]
        self.uaa_client_secret = svc_key["uaa"]["clientsecret"]
        self.uaa_url = svc_key["uaa"]["url"]

        self.uaa_token = None
        self.uaa_token_expiry = None

        self.headers = {"Content-Type": "application/json", "Authorization": None}
        self.service_url = f"{svc_key['url']}/api/v1/completions"
        self.llm_deployment_id = llm_config["DEPLOYMENT_ID"]
        self.llm_max_tokens = llm_config["MAX_TOKENS"]
        self.llm_temperature = llm_config["TEMPERATURE"]

    def _get_token(self) -> str:
        """
        Retrieves UAA client credentials token to authenticate this service to the LLM Access Service API
        """
        current_time = datetime.now(timezone.utc)
        response = requests.post(
            f"{self.uaa_url}/oauth/token",
            auth=(self.uaa_client_id, self.uaa_client_secret),
            params={"grant_type": "client_credentials"},
            timeout=REQUEST_TIMEOUT,
        )
        self.uaa_token = response.json().get("access_token", None)

        if self.uaa_token is None:
            error = response.json().get("error", None)
            print(f"ERROR WHILE GETTING UAA TOKEN: url={self.service_url}, exception={str(error)}")
            raise Exception(f"Cannot connect to UAA; response status code: {response.status_code}")

        expiry = int(response.json().get("expires_in", None))
        self.uaa_token_expiry = current_time + timedelta(seconds=expiry)
        self.headers["Authorization"] = f"Bearer {self.uaa_token}"
        return self.uaa_token

    def send_request(self, messages):
        current_time = datetime.now(timezone.utc)
        if self.uaa_token is None or current_time - self.uaa_token_expiry < timedelta(
            minutes=TOKEN_EXPIRY
        ):
            self._get_token()
        data = {
            "deployment_id": self.llm_deployment_id,
            "messages": messages,
            "max_tokens": self.llm_max_tokens,
            "temperature": self.llm_temperature,
        }
        response = None
        try:
            response = requests.post(
                self.service_url, headers=self.headers, json=data, timeout=REQUEST_TIMEOUT
            )
        except Exception as exception:
            print(
                f"ERROR WHILE CALLING GPT: url={self.service_url}, headers={json.dumps(self.headers)}, exception={str(exception)}"
            )
            raise exception
        return response
