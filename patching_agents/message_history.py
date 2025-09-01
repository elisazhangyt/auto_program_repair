from pprint import pformat

# Partially taken from autocoderover

class MessageHistory:
    """
    Represents a thread of conversation with the model.
    Abstrated into a class so that we can dump this to a file at any point.
    """

    def __init__(self, messages=None):
        self.messages: list[dict] = messages or []
    
    def add_prompt(self, role: str, message: str):
        """
        Add a new prompt to the thread.
        Args:
            message (str): The content of the new prompt.
        """
        self.messages.append({"role": "prompt", "content": message})

    def add_agent(self, role: str, message: str):
        """
        Add a new agent response to the thread.
        Args:
            message (str): The content of the new message.
            role (str): The role of the agent giving the message.
        """
        self.messages.append({"role": role, "content": message})

    def to_msg(self) -> list[dict]:
        """
        Convert to the format to be consumed by the model.
        Returns:
            List[Dict]: The message thread.
        """
        return self.messages

    def __str__(self):
        return pformat(self.messages, width=160, sort_dicts=False)

    def get_round_number(self) -> int:
        """
        From the current message history, decide how many rounds have been completed.
        """
        completed_rounds = 0
        for message in self.messages:
            if message["role"] == "assistant":
                completed_rounds += 1
        return completed_rounds