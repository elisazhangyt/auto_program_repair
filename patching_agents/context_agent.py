from cgi import test
from gpt_client import GPTClient
from message_history import MessageHistory

from typing import List

from info_dict import InfoDict

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from context_retrieval_TODO import context_retrieval as cr

class ContextAgent:
    def __init__(self, information: InfoDict):
        self.gpt_client = GPTClient()
        self.gpt_client.initialize_agent()
        self.information = information

        self.repo_path = self.information.get_info("repo path")
        self.bug_locations = self.information.get_info("bug locations")


    # print(cr.get_node_text(cr.retrieve_func_by_name(file_path, 'addItem'), code))

    def get_initial_context(self) -> tuple[str, MessageHistory]:
        self.information.add_info("buggy code", self.get_buggy_code_lines())
    
    def get_buggy_code_lines(self) -> List[int]:
        return cr.retrieve_code_by_line_number(self.repo_path, self.bug_locations)