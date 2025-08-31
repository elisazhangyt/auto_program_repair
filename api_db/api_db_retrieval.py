from asyncio import current_task
import os
import sys
import json
from typing import List, Dict

import tree_sitter_java
from tree_sitter import Language, Parser, Query


# Set up Tree-sitter parser and language
JAVA_LANGUAGE = Language(tree_sitter_java.language())
parser = Parser(JAVA_LANGUAGE)


# Retrieve all imported APIs from the original code file
def retrieve_existing_apis(java_file_path: str):
    # Read code (bytes)
    with open(java_file_path, 'rb') as f:
        code = f.read()
    tree = parser.parse(code)

    # Query for all import declarations
    query = Query(JAVA_LANGUAGE, "(import_declaration) @import")
    captures = query.captures(tree.root_node)

    # Add all import declarations to list
    imported_apis = []
    for name, nodes in captures.items():
        for node in nodes:
            snippet = code[node.start_byte:node.end_byte].decode('utf8')
            snippet = snippet[7:-1]
            imported_apis.append(snippet)

    return imported_apis


def get_api_db_path():
    # Set working directory to script's parent directory
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, ROOT_DIR)

    # Set path to API database
    API_DB_PATH = os.path.join(ROOT_DIR, "api_db.json")
    return API_DB_PATH


# Retrieve APIs by category and add to a list
def query_api_db(apis_to_retrieve: list, current_apis: list):
    API_DB_PATH = get_api_db_path()
    updated_apis = current_apis[:]

    with open(API_DB_PATH, "r", encoding="utf-8") as f:
        api_db = json.load(f)
    for api_category in apis_to_retrieve:
        if api_db[api_category][0] in updated_apis:
            continue
        else:
            for api in api_db[api_category]:
                updated_apis.append(api)
    
    return updated_apis