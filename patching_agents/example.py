import info_dict
import context_agent
import basic_agent

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

buggy_file_path = '../test_programs/chart1.java'

information = info_dict.InfoDict()
information.create_info_dict(SYSTEM_DESCRIPTION, buggy_file_path, [(1795, 1799)])

context_retriever = context_agent.ContextAgent(information)
context_retriever.get_initial_context()

basic_agent = basic_agent.BasicAgent(information)
result, msg_history = basic_agent.run("Fix the buggy code.")
print(msg_history)

