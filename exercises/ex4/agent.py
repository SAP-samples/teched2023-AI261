import json
import time

from prompt import prompt_factory


def create_ouput(title: str, output_message: str):
    result = ""
    result += "############################ "
    result += title
    result += " ###########################\n"
    if output_message is not None:
        result += output_message
    return result

def extract(d: dict, key: str) -> str:
    v = d.get(key)
    if (v is not None):
        if (len(v) > 0):
            return v
    return None


############################# Auto BDS Agent #############################
class Agent:
    def __init__(self, toolkit: dict, llm_client, agent_config: dict) -> None:
        # TODO: move most of these to be overridable in the config using env vars for kyma
        self.RECORD = agent_config["RECORD"]
        self.HISTORY_LENGTH = agent_config["HISTORY_LENGTH"]
        self.MAX_RETRIES = agent_config["MAX_RETRIES"]
        self.MAX_ITERATIONS = agent_config["MAX_ITERATIONS"]
        self.RETRY_TIMEOUT = agent_config["RETRY_TIMEOUT"]

        self.history = []
        self.toolkit = toolkit
        self.llm_client = llm_client

        self.init_prompt()

    # TODO think about a good way to do that and if that should even be a thing
    def init_prompt(self):
        self.system_message = [{"role": "system", "content": prompt_factory.get_agent_system_message(self.toolkit.keys())}]

    def _send_msg(self, streamlit, text: str):
        message = {"role": "assistant", "content": text}
        streamlit.write(text)
        streamlit.session_state.messages.append(message)


    def _add_to_history(self, history_element: dict):
        if type(history_element["content"]) != str:
            history_element["content"] = json.dumps(history_element["content"])
        self.history.append(history_element)

    # TODO build better GPT response parser
    def _parse_response(self, response_content):
        try:
            print(create_ouput("RESPONSE CONTENT", response_content))
            y = json.loads(response_content, strict=False)
            thought = extract(y, "Thought")
            action = extract(y, "Action")
            action_input = extract(y, "Action Input")
            answer = extract(y, "Answer")
            parsed = True
            observation = {"Observation": ""}
        except Exception as e:
            print(f"Output parsing error: {str(e)}")
            thought = None
            action = None
            action_input = None
            answer = None
            parsed = False
            observation = {
                "Observation": "Your response format was not correct, stick to the JSON format and write no additional text!"
            }
        return thought, action, action_input, answer, parsed, observation

    def ask_gpt(self, streamlit, user_input: str) -> list:
        # TODO: introduce token management
        if len(self.history) > self.HISTORY_LENGTH:
            self.history = self.history[-self.HISTORY_LENGTH :]

        print(create_ouput("USER INPUT", user_input))
        self._add_to_history({"role": "user", "content": user_input})

        y = {}
        iterations = 0
        retryAttempts = self.MAX_RETRIES
        while (
            (y.get("Action") is not None) or (y.get("Thought") is not None) or (len(y) == 0)
        ) and iterations < self.MAX_ITERATIONS:
            iterations += 1

            try:
                messages = self.system_message + self.history
                raw_response = self.llm_client.send_request(messages)

                while raw_response.status_code != 200:
                    print(raw_response.status_code)
                    print(raw_response.content)

                    if raw_response.status_code == 401 or raw_response.status_code == 403:
                        raise Exception(
                            "AUTHORIZATION ERROR: Failed to connect to LLM service. Please try again later."
                        )

                    retryAttempts -= 1
                    if retryAttempts <= 0:
                        print(f"MODEL OVERLOADED: Ran out of retry attempts from max {self.MAX_RETRIES}.")
                        raise Exception("There was an error generating a response. Please try again later.")
                    else:
                        # TODO: add history reduction if token limit is reached
                        self._send_msg(streamlit, f"ERROR - MODEL OVERLOADED: Sleeping for {self.RETRY_TIMEOUT} seconds before retrying.")
                        print(f"MODEL OVERLOADED: Sleeping for {self.RETRY_TIMEOUT} seconds before retrying.")
                        time.sleep(self.RETRY_TIMEOUT)
                        raw_response = self.llm_client.send_request(messages)
                model_response = raw_response.json()
                print(create_ouput("TOKENS USED", json.dumps(model_response["usage"])))
                response_content = model_response["choices"][0]["message"]["content"]
            except Exception as exception:
                print(f"ERROR WHILE CALLING GPT: {str(exception)}")
                self._send_msg(
                    streamlit, f"ERROR WHILE CALLING GPT: {str(exception)}"
                )
                return

            thought, action, action_input, answer, parsed, observation = self._parse_response(response_content)

            self._add_to_history({"role": "assistant", "content": response_content})

            if parsed:
                if thought is not None:
                    self._send_msg(streamlit, f"I think: \n{thought}")
                    observation = {
                        "Observation": "I only expressed a thought, I should use one of my available tools or write an answer."
                    }
                if action is not None:
                    print(create_ouput("ACTION", f"Running {action} with {action_input}"))
                    action_function = self.toolkit.get(action)
                    if action_function is not None:
                        try:
                            input_json = {}
                            if (action_input is not None) and (len(action_input) > 0):
                                input_json = json.loads(action_input, strict=False)
                            try:
                                observation = action_function(input_json)
                                # TODO: consider Observation Parser & UI Updater here -> make tools less smart?
                            except Exception as e:
                                observation = {"Observation": f"ERROR with tool {action}: {str(e)}"}
                        except Exception as e:
                            observation = {"Observation": f"ERROR: The Action Input has to be a correct JSON. {str(e)}"}
                    else:
                        print(f"UNKNOWN ACTION: {action}")
                        observation = {"Observation": "Unknown Action! Correct mistakes in the Action or Action Input."}

            # Only if there was an answer and no action taken, the loop will be interrupted
            # If the loop was not interrupted the last observation is added to the conversation
            if (action is None) and (answer is not None):
                self._send_msg(streamlit, f"My current answer: \n{answer}")
                break
            else:
                print(create_ouput("OBSERVATION", json.dumps(observation)))
                self._add_to_history({"role": "assistant", "content": observation})

        print(create_ouput("I FINISHED MY LOOP", None))
        self._send_msg(streamlit, "I am ready for further input now!")
        return "LOOP DONE"
