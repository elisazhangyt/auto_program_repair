SYSTEM_TASK = f"""
You are given this buggy Java code: {buggy_code_file}. Generate a patch for the bugs.

# TODO: Add a description of the bug locations.

Do not assume any methods exist unless they are explicitly called or defined.
If the patch calls a new method, it should be explicitly defined and fully implemented,
without any placeholder logic.

All buggy locations should be fixed. Refactoring and commenting should not be considered fixes.

The user cannot modify your code, so do not suggest incomplete code which requires others to modify.
Suggest the full code instead of partial code or code changes.

# TODO: Add the return format of the patch (.java file)
"""


# TODO: prompts for basic, api, repair pattern, and chain of thought agents