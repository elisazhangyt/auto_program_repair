from cgi import test
from gpt_client import GPTClient
from message_history import MessageHistory
from typing import List, Tuple

class InfoDict:
    def __init__(self):
        self.info_dict = {"system task": "", "repo path": "", "bug locations": ""}

    def create_info_dict(self, system_task: str, repo_path: str, bug_locations: List[Tuple[int, int]]):
        self.add_info("system task", system_task)
        self.add_info("repo path", repo_path)
        self.add_info("bug locations", bug_locations)

    def add_info(self, info_type, info):
        self.info_dict[info_type] = info

    def get_info(self, info_type):
        return self.info_dict[info_type]

    def format_as_prompt(self):        # Get info from self.information
        system_task = self.get_info("system task")
        buggy_code = self.get_info("buggy code")

        # Create the prompt
        return f"""
        The task of the system is: {system_task}

        You are given the following context information:
        - Buggy Code Lines: {buggy_code}
        """