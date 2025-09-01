from abc import ABC, abstractmethod
from gpt_client import GPTClient
from message_history import MessageHistory
from info_dict import InfoDict

class AbstractAgent(ABC):
    def __init__(self, information: InfoDict):
        self.information = information
        self.gpt_client = GPTClient()
        self.gpt_client.initialize_agent()
        self.msg_history = MessageHistory()

    def run(self, prompt: str) -> tuple[str, MessageHistory]:
        # TODO: fix enhanced prompt
        enhanced_prompt = self.get_prompt(prompt) + "\n" + prompt
        self.msg_history.add_user(enhanced_prompt)
        result_text = self.gpt_client.receive_response(self.gpt_client.send_prompt(enhanced_prompt))
        self.msg_history.add_model(result_text)
        return result_text, self.msg_history

    def get_prompt(self, prompt: str) -> str:
        agent_task = self.information.get_info("agent task")
        final_prompt = f"""
        The task of the agent is: {agent_task}

        Additionally, you are given the following context information about the bug:\n
        """
        final_prompt += self.format_context()
        return final_prompt
    
    @abstractmethod
    def format_context(self) -> str:
        """Abstract method - each agent must implement its own context formatting"""
        pass
