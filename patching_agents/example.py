import info_dict
from context_agent import ContextAgent
from basic_agent import BasicAgent

SYSTEM_DESCRIPTION = """
The task is to generate a patch for the buggy Java code.

Do not assume any methods exist unless they are explicitly called or defined.
If the patch calls a new method, it should be explicitly defined and fully implemented,
without any placeholder logic.

All buggy locations should be fixed. Refactoring and commenting should not be considered fixes.

The user cannot modify your code, so do not suggest incomplete code which requires others to modify.
Suggest the full code instead of partial code or code changes.

Return the patch as a .java file.
"""

BASIC_PROMPT = "Fix the buggy code."

import os
buggy_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test_programs', 'chart15.java')

information = info_dict.InfoDict()
information.create_info_dict(SYSTEM_DESCRIPTION, [(buggy_file_path, [(1379, 1379), (2051, 2052)])])

context_retriever = ContextAgent(information)

basicagent = BasicAgent(information)
result, msg_history = basicagent.run(BASIC_PROMPT)
print(msg_history)

