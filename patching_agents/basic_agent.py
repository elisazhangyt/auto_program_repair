from cgi import test
from gpt_client import GPTClient
from message_history import MessageHistory
from info_dict import InfoDict

class BasicAgent:
    def __init__(self, information: InfoDict):

        self.information = information

        self.gpt_client = GPTClient()
        self.gpt_client.initialize_agent()
        self.msg_history = MessageHistory()


    def run(self, user_prompt: str) -> tuple[str, MessageHistory]:
        enhanced_prompt = self.information.format_as_prompt() + "\n" + user_prompt
        self.msg_history.add_user(enhanced_prompt)
        result_text = self.gpt_client.receive_response(self.gpt_client.send_prompt(enhanced_prompt))
        self.msg_history.add_model(result_text)

        return result_text, self.msg_history