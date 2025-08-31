from typing import Tuple, List
from tree_sitter import Node

import isolate_bug as ib
import retrieval_utils as utils
from joern_callgraph import JoernSession

import os

# Get paths from environment variables with fallbacks
JOERN_EXECUTABLE = os.getenv('JOERN_EXECUTABLE', '/usr/local/bin/joern')
JOERN_DIRECTORY = os.getenv('JOERN_DIRECTORY', '/usr/local/share/joern')
JAVA_FILE_PATH = os.getenv('JAVA_FILE_PATH', 'test_programs/test_program.java')

'''
Types of context to retrieve:
- call graph- callee and caller sites for each buggy method/constructor
- ddg for buggy variables
'''

'''
Format of each type of context:
- file path, line number(s), content/text
'''

 # Provide a list of tuples in the form of (file path, bug locations). The bug locations should be given
 # as a list of tuples in the form of (start line number, end line number).
def format_info(all_bug_locations: List[Tuple[str, List[Tuple[int, int]]]]) -> str:
    result = ''
    bug_number = 1

    # Iterate through each file
    for buggy_file_info in all_bug_locations:
        java_file_path, bug_locations_list = buggy_file_info
        with open(java_file_path, 'rb') as f:
            code = f.read()
        bugs_in_file = ib.retrieve_buggy_lines_and_node(java_file_path, bug_locations_list)

        # Iterate through each bug in the file
        for bug_in_file in bugs_in_file:
            bug_location, bug_code, buggy_node_info = bug_in_file
            buggy_node_location, buggy_node = buggy_node_info
            comments_before_node = utils.get_comments_before_node(java_file_path, buggy_node)
            buggy_node = utils.get_node_text(buggy_node, code)
            if comments_before_node:
                comments_text = utils.get_node_text(comments_before_node, code)
            else:
                comments_text = "No comments found"
            result += f'Bug #{bug_number}:\n'
            result += f'File path: {java_file_path}\n'
            result += f'Bug line number(s): {bug_location}\n'
            result += f'Bug lines: {bug_code}'
            result += f'Buggy node line number(s): {buggy_node_location}\n'
            result += f'Buggy node: {buggy_node}\n'
            result += f'Comments before buggy node: {comments_text}\n'
            bug_number += 1
            result += '\n'
    return result


# TODO: fix json parsing
def format_callgraph_info(java_file_path: str, bug_location: Tuple[int, int]) -> str:
    # Use provided parameters or fall back to environment variables
    joern_executable = JOERN_EXECUTABLE
    joern_directory = JOERN_DIRECTORY
    
    session = JoernSession(java_file_path, joern_executable, joern_directory)
    
    # Load CPG
    if not session.load_cpg("test_program"):
        print("Failed to load CPG")
        return "Error: Could not load CPG"

    result = ''
    result += f'Caller(s) of function:\n'
    callers = session.get_function_callers(bug_location)
    for caller in callers:
        line_number, content = caller
        result += f'    - Line {line_number}: {content}\n'

    result += f'Callee(s) of function:\n'
    callees = session.get_callees_in_line_range(bug_location)
    for callee in callees:
        method_name, line_number, content = callee
        result += f'    - "{method_name}" method called at line {line_number}: {content}\n'
    
    return result


def format_ddg_info() -> str:
    # TODO
    pass