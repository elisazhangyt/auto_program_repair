from abstract_agent import AbstractAgent
import sys
import os
# Add the context_retrieval directory to the path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'context_retrieval'))
import isolate_bug as ib
import retrieval_utils as utils
from typing import Tuple

class ApiAgent(AbstractAgent):
    def get_prompt(self) -> str:
        return self.format_context()
    
    def get_agent_role(self) -> str:
        return "api"
    
    def format_context(self) -> str:
        """Format context with API database information"""
        bug_locations = self.information.get_info("bug files and locations")
        result = ''
        bug_number = 1

        # Iterate through each file
        for buggy_file_info in bug_locations:
            java_file_path, bug_locations_list = buggy_file_info
            with open(java_file_path, 'rb') as f:
                code = f.read()
            bugs_in_file = ib.retrieve_buggy_lines_and_node(java_file_path, bug_locations_list)

            # Iterate through each bug in the file
            for bug_in_file in bugs_in_file:
                bug_location, bug_code, buggy_node_info = bug_in_file
                buggy_node_location, buggy_node = buggy_node_info
                buggy_node = utils.get_node_text(buggy_node, code)
                result += f'Bug #{bug_number}:\n'
                result += f'File path: {java_file_path}\n'
                result += f'Bug line number(s): {bug_location}\n'
                result += f'Bug lines: {bug_code}'
                result += f'Buggy node line number(s): {buggy_node_location}\n'
                result += f'Buggy node: {buggy_node}\n'
                
                # API database specific additions
                result += self.format_api_database_retrieval(buggy_node_location, buggy_node)
                
                bug_number += 1
                result += '\n'
        return result
    
    def format_api_database_retrieval(self, buggy_node_location: Tuple[int, int], buggy_node: str) -> str:
        """Format API database retrieval information"""
        # TODO: Implement API database retrieval
        return "API database information: [To be implemented]\n"
    
    