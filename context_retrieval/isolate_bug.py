import tree_sitter_java
from tree_sitter import Language, Parser, Query, Node
from typing import List, Tuple
import retrieval_utils as utils

JAVA_LANGUAGE = Language(tree_sitter_java.language())

parser = Parser(JAVA_LANGUAGE)


def retrieve_buggy_lines_and_node(java_file_path: str, bug_locations: List[Tuple[int, int]]) -> List[Tuple[Tuple[int, int], str, Tuple[Tuple[int, int], Node]]]:
    result = []
    for bug_location in bug_locations:
        buggy_lines = utils.retrieve_code_by_line_number(java_file_path, bug_location)
        buggy_node = retrieve_buggy_node(java_file_path, bug_location)
        result.append((bug_location, buggy_lines, buggy_node))
    return result

# TODO: further narrow down what's provided in retrieve_buggy_class. no need to provide all method bodies


def retrieve_buggy_node(java_file_path: str, bug_location: Tuple[int, int]) -> Tuple[Tuple[int, int], Node]:
    """
    Retrieve the node that contains the buggy lines of code.
    """
    try:
        with open(java_file_path, 'rb') as f:
            code = f.read()
        tree = parser.parse(code)
    
        # Most common case: try to retrieve buggy method or constructor
        buggy_method_node = retrieve_buggy_method_or_constructor(java_file_path, bug_location)
        if buggy_method_node:
            # Convert back to 1-based line numbers for return
            node_start_line = buggy_method_node.start_point[0] + 1
            node_end_line = buggy_method_node.end_point[0] + 1
            return ((node_start_line, node_end_line), buggy_method_node)
        
        # If not in a method or constructor, the bug is most likely related to class declaration
        buggy_class_node = retrieve_buggy_class(java_file_path, bug_location)
        if buggy_class_node:
            # Convert back to 1-based line numbers for return
            node_start_line = buggy_class_node.start_point[0] + 1
            node_end_line = buggy_class_node.end_point[0] + 1
            return ((node_start_line, node_end_line), buggy_class_node)
        # TODO: figure out how to exclude irrelevant context
        
        # If not in class, it's most likely related to API importation, global variables, etc. Return None
        return None

    except FileNotFoundError:
        print(f"Error: File {java_file_path} not found")
        return None
    except Exception as e:
        print(f"Error reading file {java_file_path}: {e}")
        return None



########################################################################################
# HELPER METHODS
########################################################################################

def retrieve_buggy_method_or_constructor(java_file_path: str, bug_location: Tuple[int, int]) -> Node:
    """
    Retrieve the method declaration node that contains the buggy lines of code.
    Assumes the start and end line both fall within the range of a method_declaration node.
    """
    try:
        with open(java_file_path, 'rb') as f:
            code = f.read()
        tree = parser.parse(code)
        
        start_line, end_line = bug_location
        # Convert from 1-based to 0-based line numbers for tree-sitter
        start_line = start_line - 1
        end_line = end_line - 1
        
        # Find all method declarations
        query = Query(JAVA_LANGUAGE, """
        (method_declaration) @method_or_constructor
        (constructor_declaration) @method_or_constructor
        """)
        
        matches = query.matches(tree.root_node)
        
        # Check each method/constructor to see if it contains the bug location
        for match in matches:
            pattern_id, captures_dict = match
            nodes = captures_dict.get('method_or_constructor', [])
            
            if nodes:
                node = nodes[0]
                node_start_line = node.start_point[0]  # Line number where method/constructor starts
                node_end_line = node.end_point[0]      # Line number where method/constructor ends
                
                # Check if bug location falls within this method/constructor's range
                if node_start_line <= start_line and end_line <= node_end_line:
                    return node
        
        return None
        
    except FileNotFoundError:
        print(f"Error: File {java_file_path} not found")
        return None
    except Exception as e:
        print(f"Error reading file {java_file_path}: {e}")
        return None



def retrieve_buggy_class(java_file_path: str, bug_location: Tuple[int, int]) -> Node:
    """
    Retrieve the class declaration node that contains the buggy lines of code.
    Assumes the start and end line both fall within the range of a class_declaration node.
    """
    try:
        with open(java_file_path, 'rb') as f:
            code = f.read()
        tree = parser.parse(code)
        
        start_line, end_line = bug_location
        # Convert from 1-based to 0-based line numbers for tree-sitter
        start_line = start_line - 1
        end_line = end_line - 1
        
        # Find all class declarations
        query = Query(JAVA_LANGUAGE, """
        (class_declaration) @class
        """)
        
        matches = query.matches(tree.root_node)
        
        # Check each class to see if it contains the bug location
        for match in matches:
            pattern_id, captures_dict = match
            class_nodes = captures_dict.get('class', [])
            
            if class_nodes:
                class_node = class_nodes[0]
                class_start = class_node.start_point[0]  # Line number where class starts
                class_end = class_node.end_point[0]      # Line number where class ends
                
                # Check if bug location falls within this class's range
                if class_start <= start_line and end_line <= class_end:
                    return class_node
        
        return None
        
    except FileNotFoundError:
        print(f"Error: File {java_file_path} not found")
        return None
    except Exception as e:
        print(f"Error reading file {java_file_path}: {e}")
        return None